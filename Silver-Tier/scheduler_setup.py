"""
scheduler_setup.py — Registers all watchers with Windows Task Scheduler.
Run ONCE as Administrator: python scheduler_setup.py

This makes all watchers start automatically without you doing anything.
"""

import os
import subprocess
import sys

# ── CONFIGURE ────────────────────────────────────────────────────────────────
# Path to your Silver-Tier folder
PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
PYTHON_EXE   = sys.executable   # Auto-detects your Python path
# ─────────────────────────────────────────────────────────────────────────────


def create_task(task_name: str, script: str, schedule: str, extra_args: str = ""):
    """Creates a Windows Task Scheduler task."""
    script_path = os.path.join(PROJECT_PATH, script)
    
    # Wrap paths in escaped quotes to handle spaces
    command = f'\\"{PYTHON_EXE}\\" \\"{script_path}\\"'

    cmd = (
        f'schtasks /create /tn "{task_name}" '
        f'/tr "{command}" '
        f'{schedule} '
        f'/ru "{os.environ.get("USERNAME", "")}" '
        f'/f'
    )

    print(f"\n📅 Creating task: {task_name}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    if result.returncode == 0:
        print(f"   ✅ Task created successfully")
    else:
        print(f"   ❌ Failed: {result.stderr.strip()}")

    return result.returncode == 0


def main():
    print("=" * 60)
    print("🚀 Setting up Windows Task Scheduler for Silver Tier")
    print("=" * 60)

    tasks = [
        {
            "name": "PersonalAI_GmailWatcher",
            "script": "gmail_watcher.py",
            # Run at login, then repeat every 2 minutes
            "schedule": '/sc onlogon /delay 0001:00'
        },
        {
            "name": "PersonalAI_WhatsAppWatcher",
            "script": "whatsapp_watcher.py",
            "schedule": '/sc onlogon /delay 0002:00'
        },
        {
            "name": "PersonalAI_ApprovalHandler",
            "script": "approval_handler.py",
            "schedule": '/sc onlogon /delay 0000:30'
        },
        {
            "name": "PersonalAI_LinkedInPoster",
            "script": "linkedin_poster.py",
            # Run daily at 9:00 AM
            "schedule": '/sc daily /st 09:00'
        },
    ]

    success_count = 0
    for task in tasks:
        ok = create_task(task["name"], task["script"], task["schedule"])
        if ok:
            success_count += 1

    print(f"\n{'=' * 60}")
    print(f"✨ Done! {success_count}/{len(tasks)} tasks registered")
    print(f"\nTo verify: Open Task Scheduler → Task Scheduler Library")
    print(f"Look for tasks starting with 'PersonalAI_'")
    print(f"\nTo run a task now: Right-click → Run")
    print(f"To remove a task: Right-click → Delete")
    print(f"{'=' * 60}\n")


if __name__ == "__main__":
    main()
