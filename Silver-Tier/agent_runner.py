"""
agent_runner.py — The brain of the Personal AI Employee.
Called by watcher.py when a new file appears in /Inbox.

Usage: python agent_runner.py /path/to/inbox/file.txt
"""

import os
import sys
import json
import shutil
import subprocess
import logging
from datetime import datetime, timezone

# ── CONFIGURE THIS ────────────────────────────────────────────────────────────
VAULT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "PersonalAI_Vault")

# How you call Qwen on your machine. Common options:
#   "qwen"          → if installed as CLI tool
#   "ollama run qwen2.5"   → if using Ollama locally
# This script also supports Qwen via API (set USE_API = True below)
QWEN_COMMAND = ["qwen", "chat"]   # ← CHANGE THIS to match your Qwen setup

# Set to True if you want to use Qwen's HTTP API instead of CLI
USE_API = False
QWEN_API_URL = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
QWEN_API_KEY = os.environ.get("QWEN_API_KEY", "")   # set in your environment
# ─────────────────────────────────────────────────────────────────────────────

INBOX_PATH       = os.path.join(VAULT_PATH, "Inbox")
NEEDS_ACTION_PATH= os.path.join(VAULT_PATH, "Needs_Action")
DONE_PATH        = os.path.join(VAULT_PATH, "Done")
HANDBOOK_PATH    = os.path.join(VAULT_PATH, "Company_Handbook.md")
TRIAGE_SKILL_PATH= os.path.join(VAULT_PATH, "Skills", "skill_triage.md")
DASHBOARD_PATH   = os.path.join(VAULT_PATH, "Dashboard.md")
LOG_PATH         = os.path.join(VAULT_PATH, "Logs", "watcher.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_PATH, encoding="utf-8"),
        logging.StreamHandler()
    ]
)
log = logging.getLogger("AgentRunner")


# ──────────────────────────────────────────────────────────────────────────────
# STEP 1: Read supporting files
# ──────────────────────────────────────────────────────────────────────────────

def read_file(path: str) -> str:
    """Safely reads a file and returns its contents."""
    for encoding in ["utf-8", "utf-16", "utf-8-sig", "latin-1"]:
        try:
            with open(path, "r", encoding=encoding) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    log.error(f"Could not read file with any encoding: {path}")
    return ""


# ──────────────────────────────────────────────────────────────────────────────
# STEP 2: Build the prompt
# ──────────────────────────────────────────────────────────────────────────────

def build_prompt(inbox_content: str, filename: str) -> str:
    """Constructs the full prompt for Qwen."""
    handbook = read_file(HANDBOOK_PATH)
    triage_skill = read_file(TRIAGE_SKILL_PATH)

    prompt = f"""You are a Personal AI Employee. You must follow all rules in the Company Handbook strictly.

=== COMPANY HANDBOOK (YOUR RULES) ===
{handbook}

=== TRIAGE SKILL (HOW TO PROCESS THIS ITEM) ===
{triage_skill}

=== YOUR TASK ===
A new item has arrived in the Inbox. Analyze it and respond using the EXACT output format
described in the Triage Skill. Do not add extra commentary outside the format.

Filename: {filename}
Timestamp: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")}

=== INBOX ITEM CONTENT ===
{inbox_content}

=== YOUR STRUCTURED RESPONSE (follow the template exactly) ==="""

    return prompt


# ──────────────────────────────────────────────────────────────────────────────
# STEP 3: Call Qwen
# ──────────────────────────────────────────────────────────────────────────────

def call_qwen_cli(prompt: str) -> str:
    """Calls Qwen via CLI subprocess and returns the response text."""
    print("=== CALLING QWEN ===")
    print(f"Prompt length: {len(prompt)}")
    
    log.info("🧠 Calling Qwen CLI...")
    try:
        result = subprocess.run(
            "qwen chat",
            input=prompt,
            capture_output=True,
            text=True,
            timeout=90,
            shell=True,
            encoding="utf-8",
            errors="replace"
        )
        print(f"Qwen result: {result.stdout[:200]}")
        print(f"Return code: {result.returncode}")
        
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
        else:
            log.error(f"Qwen stderr: {result.stderr}")
            return f"[ERROR] Qwen returned empty. stderr: {result.stderr}"
    except Exception as e:
        return f"[ERROR] {e}"

def call_qwen_api(prompt: str) -> str:
    """Calls Qwen via HTTP API. Used when USE_API = True."""
    import urllib.request
    log.info("🧠 Calling Qwen API...")

    payload = json.dumps({
        "model": "qwen-plus",
        "input": {
            "messages": [
                {"role": "system", "content": "You are a helpful personal AI employee."},
                {"role": "user", "content": prompt}
            ]
        }
    }).encode("utf-8")

    req = urllib.request.Request(
        QWEN_API_URL,
        data=payload,
        headers={
            "Authorization": f"Bearer {QWEN_API_KEY}",
            "Content-Type": "application/json"
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["output"]["text"]
    except Exception as e:
        log.error(f"API call failed: {e}")
        return f"[ERROR] API call failed: {e}"


def call_qwen(prompt: str) -> str:
    if USE_API:
        return call_qwen_api(prompt)
    return call_qwen_cli(prompt)


# ──────────────────────────────────────────────────────────────────────────────
# STEP 4: Write output to /Needs_Action
# ──────────────────────────────────────────────────────────────────────────────

def write_needs_action(filename: str, qwen_response: str) -> str:
    """Saves Qwen's structured response to /Needs_Action."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = os.path.splitext(filename)[0]
    output_filename = f"{base_name}_response_{timestamp}.md"
    output_path = os.path.join(NEEDS_ACTION_PATH, output_filename)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(qwen_response)

    log.info(f"📝 Response written to /Needs_Action/{output_filename}")
    return output_path


# ──────────────────────────────────────────────────────────────────────────────
# STEP 5: Update Dashboard.md
# ──────────────────────────────────────────────────────────────────────────────

def update_dashboard(filename: str, qwen_response: str):
    """Updates Dashboard.md with current stats."""
    inbox_count  = len([f for f in os.listdir(INBOX_PATH) if os.path.isfile(os.path.join(INBOX_PATH, f))])
    action_count = len([f for f in os.listdir(NEEDS_ACTION_PATH) if os.path.isfile(os.path.join(NEEDS_ACTION_PATH, f))])
    done_count   = len([f for f in os.listdir(DONE_PATH) if os.path.isfile(os.path.join(DONE_PATH, f))])

    # Try to extract urgency from response
    urgency = "🟡 NORMAL"
    if "URGENT" in qwen_response.upper():
        urgency = "🔴 URGENT"
    elif "LOW" in qwen_response.upper():
        urgency = "🟢 LOW"

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Read last 5 lines of log for activity feed
    try:
        with open(LOG_PATH, "r", encoding="utf-8") as f:
            lines = f.readlines()
        recent = "".join(lines[-5:]) if len(lines) >= 5 else "".join(lines)
    except:
        recent = "No log data yet."

    dashboard = f"""# 🤖 AI Employee Dashboard
*Last updated: {timestamp}*

---

## 📊 Current Status

| Metric           | Count          |
|------------------|----------------|
| 📥 Inbox Items   | {inbox_count}  |
| ⚡ Needs Action  | {action_count} |
| ✅ Done Today    | {done_count}   |

---

## 🧠 Last AI Action
> **Processed:** `{filename}`
> **Classification:** {urgency}
> **Time:** {timestamp}

---

## 📋 Recent Agent Log
```
{recent}
```

---

## 🎯 Status
**Agent:** 🟢 Online
**Watcher:** 🟢 Running
**Last Run:** {timestamp}
"""

    with open(DASHBOARD_PATH, "w", encoding="utf-8") as f:
        f.write(dashboard)

    log.info("📊 Dashboard.md updated")


# ──────────────────────────────────────────────────────────────────────────────
# STEP 6: Move file to /Done
# ──────────────────────────────────────────────────────────────────────────────

def archive_file(filepath: str):
    """Moves processed file from /Inbox to /Done."""
    filename = os.path.basename(filepath)
    dest = os.path.join(DONE_PATH, filename)
    shutil.move(filepath, dest)
    log.info(f"📦 Archived to /Done: {filename}")


# ──────────────────────────────────────────────────────────────────────────────
# MAIN ORCHESTRATION
# ──────────────────────────────────────────────────────────────────────────────

def run(filepath: str):
    print("=== AGENT RUNNER STARTED ===")
    print(f"Processing file: {filepath}")
    
    filename = os.path.basename(filepath)
    log.info(f"═══════════════════════════════════════")
    log.info(f"▶  Processing: {filename}")

    # 1. Read inbox file
    inbox_content = read_file(filepath)
    if not inbox_content.strip():
        log.warning(f"⚠  File is empty, skipping: {filename}")
        return

    # 2. Build prompt
    prompt = build_prompt(inbox_content, filename)

    # 3. Call Qwen
    response = call_qwen(prompt)
    log.info(f"🗣  Qwen responded ({len(response)} chars)")

    # Check if this is an email request
    email_keywords = ["send an email", "email to", "write an email"]
    is_email_request = any(kw in inbox_content.lower() for kw in email_keywords)

    print(f"EMAIL DETECTED: {is_email_request}")
    print(f"Inbox content preview: {inbox_content[:100]}")

    if is_email_request:
        # Extract email address from content
        import re
        email_match = re.search(r'[\w.-]+@[\w.-]+\.\w+', inbox_content)
        to_email = email_match.group() if email_match else "unknown@email.com"

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        email_filename = f"DRAFT_EMAIL_{timestamp}.md"
        filepath_email = os.path.join(NEEDS_ACTION_PATH, "APPROVAL_REQUIRED", email_filename)

        print(f"Writing email draft to: {filepath_email}")

        draft_content = f"""**To:** {to_email}
**Subject:** Ramadan Prompting Night by Asharib Ali
**Action:** SEND_EMAIL

## Draft Body:
{response}

---
## To Approve: Rename to APPROVED_{email_filename}
## To Reject: Rename to REJECTED_{email_filename}
"""
        with open(filepath_email, "w", encoding="utf-8") as f:
            f.write(draft_content)
        
        # Skip normal needs_action write
        archive_file(filepath)
        update_dashboard(filename, response)
        log.info(f"📧 Email draft created: {email_filename}")
        return

    # 4. Write to /Needs_Action
    write_needs_action(filename, response)

    # 5. Update Dashboard
    update_dashboard(filename, response)

    # 6. Archive original
    archive_file(filepath)

    log.info(f"✅ Done: {filename}")
    log.info(f"═══════════════════════════════════════")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python agent_runner.py /path/to/inbox/file.txt")
        sys.exit(1)

    target_file = sys.argv[1]

    if not os.path.exists(target_file):
        print(f"File not found: {target_file}")
        sys.exit(1)

    run(target_file)
