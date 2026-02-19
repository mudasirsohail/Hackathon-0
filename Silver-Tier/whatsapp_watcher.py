"""
whatsapp_watcher.py — Monitors WhatsApp Web for keyword messages.
Run: python whatsapp_watcher.py
First run: Chromium opens, scan QR code with your phone. Session saved after that.
"""

import os
import json
from pathlib import Path
from datetime import datetime
from base_watcher import BaseWatcher

# ── CONFIGURE ────────────────────────────────────────────────────────────────
SESSION_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "PersonalAI_Vault", "credentials", "whatsapp_session"
)

TRIGGER_KEYWORDS = ["urgent", "asap", "invoice", "payment", "help", "deadline", "meeting"]
# ─────────────────────────────────────────────────────────────────────────────


class WhatsAppWatcher(BaseWatcher):

    def __init__(self):
        super().__init__(name="WhatsAppWatcher", check_interval=30)
        self.session_path = SESSION_PATH
        self.processed_messages = self._load_processed()
        os.makedirs(self.session_path, exist_ok=True)

    def _load_processed(self) -> set:
        p = Path(os.path.dirname(os.path.abspath(__file__))) / "PersonalAI_Vault" / "credentials" / "processed_wa.json"
        if p.exists():
            with open(p) as f:
                return set(json.load(f))
        return set()

    def _save_processed(self):
        p = Path(os.path.dirname(os.path.abspath(__file__))) / "PersonalAI_Vault" / "credentials" / "processed_wa.json"
        with open(p, "w") as f:
            json.dump(list(self.processed_messages), f)

    def check_for_updates(self) -> list:
        """Opens WhatsApp Web and scans for keyword messages."""
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            self.logger.error("Run: pip install playwright && playwright install chromium")
            return []

        found_messages = []

        try:
            with sync_playwright() as p:
                browser = p.chromium.launch_persistent_context(
                    self.session_path,
                    headless=False,
                    args=["--no-sandbox"],
                    viewport={"width": 1280, "height": 800}
                )

                page = browser.pages[0] if browser.pages else browser.new_page()
                page.goto("https://web.whatsapp.com", timeout=60000)
                self.logger.info("Waiting for WhatsApp to load...")

                # Wait for sidebar
                page.wait_for_selector('#pane-side', timeout=60000)
                page.wait_for_timeout(4000)
                self.logger.info("WhatsApp loaded!")

                # Use JavaScript to extract all chat text directly
                chat_texts = page.evaluate("""
                    () => {
                        const results = [];
                        const sidebar = document.querySelector('#pane-side');
                        if (!sidebar) return results;
                        
                        // Get all divs that look like chat rows
                        const allDivs = sidebar.querySelectorAll('div[role="listitem"], div[tabindex="-1"]');
                        allDivs.forEach(div => {
                            const text = div.innerText;
                            if (text && text.length > 3) {
                                results.push(text);
                            }
                        });
                        return results;
                    }
                """)

                self.logger.info(f"Found {len(chat_texts)} chat elements via JavaScript")

                for text in chat_texts:
                    text_lower = text.lower()
                    lines = text.split("\n")
                    sender = lines[0] if lines else "Unknown"

                    for kw in TRIGGER_KEYWORDS:
                        if kw in text_lower:
                            fingerprint = f"{sender}:{text_lower[:50]}"
                            if fingerprint not in self.processed_messages:
                                found_messages.append({
                                    "sender": sender,
                                    "text": text[:500],
                                    "keyword": kw,
                                    "fingerprint": fingerprint
                                })
                                self.logger.info(f"Keyword '{kw}' found in chat: {sender}")
                            break

                browser.close()

        except Exception as e:
            self.logger.error(f"WhatsApp error: {e}")

        return found_messages

    def create_action_file(self, message: dict) -> Path:
        """Creates a structured .md file in /Needs_Action for a WhatsApp message."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        safe_sender = message["sender"].replace(" ", "_").replace("/", "-").replace("\\", "-").replace(":", "")[:20]

        content = f"""---
type: whatsapp
from: {message['sender']}
keyword: {message['keyword']}
received: {timestamp}
status: pending
---

# WhatsApp Message from {message['sender']}

**From:** {message['sender']}
**Keyword Triggered:** {message['keyword']}
**Received:** {timestamp}

---

## Message Content
{message['text']}

---

## Suggested Actions
- [ ] Reply to sender
- [ ] Escalate if payment/invoice related
- [ ] Archive after handling

---
Processed by WhatsApp Watcher at {timestamp}
"""

        filename = f"WHATSAPP_{safe_sender}_{datetime.now().strftime('%H%M%S')}.md"
        filepath = self.write_action_file(filename, content)

        self.processed_messages.add(message["fingerprint"])
        self._save_processed()

        return filepath


if __name__ == "__main__":
    watcher = WhatsAppWatcher()
    watcher.run()
