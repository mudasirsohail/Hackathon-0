"""
gmail_watcher.py — Monitors Gmail for unread important emails.
Run: python gmail_watcher.py
Checks every 2 minutes. First run opens browser for Google login.
"""

import os
import json
import base64
from pathlib import Path
from datetime import datetime
from base_watcher import BaseWatcher

# ── CONFIGURE ────────────────────────────────────────────────────────────────
CREDENTIALS_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "PersonalAI_Vault", "credentials", "gmail_credentials.json"
)
TOKEN_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "PersonalAI_Vault", "credentials", "token.json"
)
# ─────────────────────────────────────────────────────────────────────────────

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.modify"
]


class GmailWatcher(BaseWatcher):

    def __init__(self):
        super().__init__(name="GmailWatcher", check_interval=120)  # Every 2 minutes
        self.processed_ids = self._load_processed_ids()
        self.service = self._authenticate()

    def _load_processed_ids(self) -> set:
        """Load already-processed email IDs so we don't duplicate."""
        ids_file = Path(os.path.dirname(os.path.abspath(__file__))) / "PersonalAI_Vault" / "credentials" / "processed_emails.json"
        if ids_file.exists():
            with open(ids_file, "r") as f:
                return set(json.load(f))
        return set()

    def _save_processed_ids(self):
        """Persist processed IDs to disk."""
        ids_file = Path(os.path.dirname(os.path.abspath(__file__))) / "PersonalAI_Vault" / "credentials" / "processed_emails.json"
        with open(ids_file, "w") as f:
            json.dump(list(self.processed_ids), f)

    def _authenticate(self):
        """Handles Google OAuth2. Opens browser on first run."""
        try:
            from google.oauth2.credentials import Credentials
            from google_auth_oauthlib.flow import InstalledAppFlow
            from google.auth.transport.requests import Request
            from googleapiclient.discovery import build
        except ImportError:
            self.logger.error("❌ Missing packages! Run: pip install google-auth google-auth-oauthlib google-api-python-client")
            return None

        creds = None

        # Load existing token
        if os.path.exists(TOKEN_PATH):
            creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

        # If no valid token, do OAuth flow
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
                self.logger.info("🔄 Token refreshed automatically")
            else:
                if not os.path.exists(CREDENTIALS_PATH):
                    self.logger.error(f"❌ gmail_credentials.json not found at: {CREDENTIALS_PATH}")
                    self.logger.error("Download it from Google Cloud Console → APIs → Credentials")
                    return None

                self.logger.info("🌐 Opening browser for Google login (one time only)...")
                flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
                creds = flow.run_local_server(port=0)

            # Save token for future runs
            with open(TOKEN_PATH, "w") as f:
                f.write(creds.to_json())
            self.logger.info("✅ Token saved. No login needed next time.")

        return build("gmail", "v1", credentials=creds)

    def check_for_updates(self) -> list:
        """Fetches unread important emails not yet processed."""
        if not self.service:
            return []

        try:
            results = self.service.users().messages().list(
                userId="me",
                q="is:unread is:important",
                maxResults=10
            ).execute()

            messages = results.get("messages", [])
            new_messages = [m for m in messages if m["id"] not in self.processed_ids]
            self.logger.info(f"📬 Found {len(new_messages)} new important emails")
            return new_messages

        except Exception as e:
            self.logger.error(f"Gmail API error: {e}")
            return []

    def create_action_file(self, message: dict) -> Path:
        """Fetches full email details and creates structured .md in /Needs_Action."""
        try:
            msg = self.service.users().messages().get(
                userId="me",
                id=message["id"],
                format="full"
            ).execute()

            # Extract headers
            headers = {}
            for h in msg["payload"].get("headers", []):
                headers[h["name"]] = h["value"]

            sender   = headers.get("From", "Unknown")
            subject  = headers.get("Subject", "No Subject")
            date     = headers.get("Date", datetime.now().isoformat())
            snippet  = msg.get("snippet", "")

            # Try to get full body
            body = self._extract_body(msg)

            content = f"""---
type: email
from: {sender}
subject: {subject}
received: {date}
email_id: {message['id']}
priority: high
status: pending
---

# 📧 Email: {subject}

**From:** {sender}
**Received:** {date}

---

## Email Content
{snippet}

{body}

---

## Suggested Actions
- [ ] Reply to sender
- [ ] Forward to relevant party
- [ ] Archive after processing

---
*Processed by Gmail Watcher at {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
"""

            filename = f"EMAIL_{message['id'][:12]}_{datetime.now().strftime('%H%M%S')}.md"
            filepath = self.write_action_file(filename, content)

            # Mark as read
            self.service.users().messages().modify(
                userId="me",
                id=message["id"],
                body={"removeLabelIds": ["UNREAD"]}
            ).execute()

            # Track as processed
            self.processed_ids.add(message["id"])
            self._save_processed_ids()

            return filepath

        except Exception as e:
            self.logger.error(f"Error processing email {message['id']}: {e}")
            raise

    def _extract_body(self, msg: dict) -> str:
        """Tries to extract plain text body from email."""
        try:
            parts = msg["payload"].get("parts", [])
            for part in parts:
                if part["mimeType"] == "text/plain":
                    data = part["body"].get("data", "")
                    if data:
                        return base64.urlsafe_b64decode(data).decode("utf-8")
            return ""
        except:
            return ""


if __name__ == "__main__":
    watcher = GmailWatcher()
    watcher.run()
