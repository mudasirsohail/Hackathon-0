"""
watcher.py — Monitors /Inbox for new files and triggers the AI agent.
Run: python watcher.py
Keep this running in the background.
"""

import os
import time
import logging
import subprocess
from datetime import datetime, timezone
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# ── CONFIGURE THIS ────────────────────────────────────────────────────────────
VAULT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "PersonalAI_Vault")
# ─────────────────────────────────────────────────────────────────────────────

INBOX_PATH = os.path.join(VAULT_PATH, "Inbox")
LOG_PATH   = os.path.join(VAULT_PATH, "Logs", "watcher.log")

# Set up logging to both console and log file
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_PATH, encoding="utf-8"),
        logging.StreamHandler()
    ]
)
log = logging.getLogger("Watcher")


class InboxHandler(FileSystemEventHandler):
    """Fires when a file is created in /Inbox."""

    def on_created(self, event):
        if event.is_directory:
            return

        filepath = event.src_path
        filename = os.path.basename(filepath)

        # Only process .txt and .md files
        if not (filename.endswith(".txt") or filename.endswith(".md")):
            log.info(f"Ignored non-text file: {filename}")
            return

        # Small delay to ensure file is fully written before reading
        time.sleep(1)

        log.info(f"📥 New file detected: {filename}")
        trigger_agent(filepath)


def trigger_agent(filepath: str):
    """Calls agent_runner.py with the new file path."""
    log.info(f"🤖 Triggering agent for: {filepath}")
    try:
        result = subprocess.run(
            ["python", "agent_runner.py", filepath],
            capture_output=True,
            text=True,
            timeout=120   # 2 minute timeout per file
        )
        if result.returncode == 0:
            log.info(f"✅ Agent completed successfully for: {os.path.basename(filepath)}")
        else:
            log.error(f"❌ Agent failed: {result.stderr}")
    except subprocess.TimeoutExpired:
        log.error(f"⏱ Agent timed out for: {filepath}")
    except Exception as e:
        log.error(f"💥 Unexpected error: {e}")


def main():
    log.info("=" * 60)
    log.info("🚀 PersonalAI Watcher starting up...")
    log.info(f"👁  Monitoring: {INBOX_PATH}")
    log.info("Drop any .txt or .md file into /Inbox to trigger the AI")
    log.info("Press Ctrl+C to stop")
    log.info("=" * 60)

    if not os.path.exists(INBOX_PATH):
        log.error(f"❌ Inbox folder not found: {INBOX_PATH}")
        log.error("Run: python setup_vault.py first!")
        return

    event_handler = InboxHandler()
    observer = Observer()
    observer.schedule(event_handler, path=INBOX_PATH, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(2)
    except KeyboardInterrupt:
        log.info("🛑 Watcher stopped by user.")
        observer.stop()
    observer.join()


if __name__ == "__main__":
    main()
