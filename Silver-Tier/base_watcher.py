"""
base_watcher.py — Parent class for all Silver Tier watchers.
All watchers (Gmail, WhatsApp) inherit from this.
"""

import time
import logging
import os
from pathlib import Path
from abc import ABC, abstractmethod
from datetime import datetime

VAULT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "PersonalAI_Vault")


def setup_logger(name: str, log_file: str) -> logging.Logger:
    """Creates a logger that writes to both console and a log file."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

    # File handler
    fh = logging.FileHandler(log_file, encoding="utf-8")
    fh.setFormatter(formatter)

    # Console handler
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger


class BaseWatcher(ABC):
    """
    Abstract base class for all watchers.
    Subclasses must implement check_for_updates() and create_action_file().
    """

    def __init__(self, name: str, check_interval: int = 60):
        self.name = name
        self.vault_path = Path(VAULT_PATH)
        self.needs_action = self.vault_path / "Needs_Action"
        self.approval_required = self.needs_action / "APPROVAL_REQUIRED"
        self.done_path = self.vault_path / "Done"
        self.check_interval = check_interval

        # Setup logger
        log_file = str(self.vault_path / "Logs" / f"{name.lower()}_watcher.log")
        self.logger = setup_logger(name, log_file)

    @abstractmethod
    def check_for_updates(self) -> list:
        """
        Check the source (Gmail, WhatsApp, etc.) for new items.
        Returns a list of new items to process.
        """
        pass

    @abstractmethod
    def create_action_file(self, item) -> Path:
        """
        Takes a new item and creates a structured .md file in /Needs_Action.
        Returns the path of the created file.
        """
        pass

    def run(self):
        """Main loop — runs forever, checking for updates on interval."""
        self.logger.info("=" * 50)
        self.logger.info(f"🚀 {self.name} starting up...")
        self.logger.info(f"⏱  Check interval: {self.check_interval} seconds")
        self.logger.info("Press Ctrl+C to stop")
        self.logger.info("=" * 50)

        while True:
            try:
                self.logger.info(f"🔍 Checking for new items...")
                items = self.check_for_updates()

                if items:
                    self.logger.info(f"📥 Found {len(items)} new item(s)")
                    for item in items:
                        filepath = self.create_action_file(item)
                        self.logger.info(f"✅ Created action file: {filepath.name}")
                        self.trigger_agent(filepath)
                else:
                    self.logger.info(f"😴 Nothing new. Sleeping {self.check_interval}s...")

            except KeyboardInterrupt:
                self.logger.info(f"🛑 {self.name} stopped by user.")
                break
            except Exception as e:
                self.logger.error(f"💥 Error in {self.name}: {e}")

            time.sleep(self.check_interval)

    def trigger_agent(self, filepath: Path):
        """Calls agent_runner.py to process the new action file."""
        import subprocess
        agent_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "agent_runner.py")
        try:
            subprocess.Popen(
                ["python", agent_script, str(filepath)],
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
            )
            self.logger.info(f"🤖 Agent triggered for: {filepath.name}")
        except Exception as e:
            self.logger.error(f"Failed to trigger agent: {e}")

    def write_action_file(self, filename: str, content: str) -> Path:
        """Helper — writes content to /Needs_Action and returns the path."""
        filepath = self.needs_action / filename
        filepath.write_text(content, encoding="utf-8")
        return filepath

    def write_approval_file(self, filename: str, content: str) -> Path:
        """Helper — writes content to /Needs_Action/APPROVAL_REQUIRED/"""
        filepath = self.approval_required / filename
        filepath.write_text(content, encoding="utf-8")
        self.logger.info(f"⏳ Approval required: {filename}")
        return filepath
