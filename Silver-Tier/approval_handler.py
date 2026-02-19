"""
approval_handler.py — Watches APPROVAL_REQUIRED folder for human decisions.

HOW IT WORKS:
1. AI writes a draft to /Needs_Action/APPROVAL_REQUIRED/DRAFT_xxx.md
2. Human reviews it in Obsidian or File Explorer
3. Human renames it to:
   - APPROVED_xxx.md  → handler executes the action
   - REJECTED_xxx.md  → handler archives it, no action taken
4. Handler moves the file to /Done/

Run alongside your watchers: python approval_handler.py
"""

import os
import time
import shutil
import smtplib
import logging
from pathlib import Path
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ── CONFIGURE ────────────────────────────────────────────────────────────────
VAULT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "PersonalAI_Vault")

# Gmail SMTP settings for sending emails
SMTP_EMAIL    = os.environ.get("SMTP_EMAIL", "your_email@gmail.com")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD", "")   # Use App Password, not real password
SMTP_SERVER   = "smtp.gmail.com"
SMTP_PORT     = 587
# ─────────────────────────────────────────────────────────────────────────────

APPROVAL_PATH = os.path.join(VAULT_PATH, "Needs_Action", "APPROVAL_REQUIRED")
DONE_PATH     = os.path.join(VAULT_PATH, "Done")
LOG_PATH      = os.path.join(VAULT_PATH, "Logs", "approval_handler.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_PATH, encoding="utf-8"),
        logging.StreamHandler()
    ]
)
log = logging.getLogger("ApprovalHandler")


def parse_action_file(filepath: Path) -> dict:
    """Reads an approval file and extracts the action type and content."""
    content = filepath.read_text(encoding="utf-8")
    lines = content.split("\n")

    action = {
        "type": "unknown",
        "to": "",
        "subject": "",
        "body": "",
        "post_content": "",
        "raw": content
    }

    # Parse frontmatter-style fields
    for line in lines:
        if line.startswith("**To:**"):
            action["to"] = line.replace("**To:**", "").strip()
        elif line.startswith("**Subject:**"):
            action["subject"] = line.replace("**Subject:**", "").strip()
        elif line.startswith("**Action:**"):
            action_type = line.replace("**Action:**", "").strip()
            action["type"] = action_type

    # Extract body (everything after "## Draft Email for Approval:" or "## Draft Body:")
    if "## Draft Email for Approval:" in content:
        action["body"] = content.split("## Draft Email for Approval:")[-1].strip()
        action["body"] = action["body"].split("---")[0].strip()
        action["type"] = "SEND_EMAIL"
    elif "## Draft Body:" in content:
        action["body"] = content.split("## Draft Body:")[-1].strip()
        action["body"] = action["body"].split("---")[0].strip()
        action["type"] = "SEND_EMAIL"

    if "## Post Content:" in content:
        action["post_content"] = content.split("## Post Content:")[-1].strip()
        action["post_content"] = action["post_content"].split("---")[0].strip()
        action["type"] = "LINKEDIN_POST"

    return action


def send_email(to: str, subject: str, body: str) -> bool:
    """Sends an email via Gmail SMTP."""
    if not SMTP_PASSWORD:
        log.error("❌ SMTP_PASSWORD not set! Set environment variable SMTP_PASSWORD")
        log.error("Use Gmail App Password: myaccount.google.com → Security → App Passwords")
        return False

    try:
        msg = MIMEMultipart()
        msg["From"]    = SMTP_EMAIL
        msg["To"]      = to
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.send_message(msg)

        log.info(f"📧 Email sent to: {to} | Subject: {subject}")
        return True

    except Exception as e:
        log.error(f"Email send failed: {e}")
        return False


def post_to_linkedin(content: str) -> bool:
    """Posts content to LinkedIn using Playwright browser automation."""
    # Import from linkedin_poster.py
    from linkedin_poster import post_via_playwright
    
    log.info("💼 Executing: Post to LinkedIn via Playwright")
    return post_via_playwright(content)


def execute_action(action: dict, filename: str) -> bool:
    """Executes the approved action based on its type."""
    action_type = action["type"]

    if action_type == "SEND_EMAIL":
        log.info(f"📧 Executing: Send email to {action['to']}")
        return send_email(action["to"], action["subject"], action["body"])

    elif action_type == "LINKEDIN_POST":
        log.info(f"💼 Executing: Post to LinkedIn")
        from linkedin_poster import post_via_playwright
        return post_via_playwright(action["post_content"])

    else:
        log.warning(f"⚠ Unknown action type: {action_type} in {filename}")
        return False


def archive_file(filepath: Path, prefix: str):
    """Moves file to /Done with a timestamp prefix."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dest = os.path.join(DONE_PATH, f"{prefix}_{timestamp}_{filepath.name}")
    shutil.move(str(filepath), dest)
    log.info(f"📦 Archived to /Done: {filepath.name}")


def scan_for_decisions():
    """Scans APPROVAL_REQUIRED for APPROVED_ or REJECTED_ files."""
    approval_dir = Path(APPROVAL_PATH)

    for filepath in approval_dir.iterdir():
        if not filepath.is_file():
            continue

        name = filepath.name

        if name.startswith("APPROVED_"):
            log.info(f"✅ APPROVED: {name}")
            action = parse_action_file(filepath)
            success = execute_action(action, name)
            archive_file(filepath, "EXECUTED" if success else "FAILED")

        elif name.startswith("REJECTED_"):
            log.info(f"❌ REJECTED: {name} — No action taken")
            archive_file(filepath, "REJECTED")


def main():
    log.info("=" * 55)
    log.info("⏳ Approval Handler running...")
    log.info(f"👁  Watching: {APPROVAL_PATH}")
    log.info("Rename files to APPROVED_xxx.md or REJECTED_xxx.md")
    log.info("=" * 55)

    while True:
        try:
            scan_for_decisions()
        except Exception as e:
            log.error(f"Error in scan: {e}")
        time.sleep(3)   # Check every 3 seconds


if __name__ == "__main__":
    main()
