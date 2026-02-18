"""
setup_vault.py — Auto-creates the PersonalAI_Vault structure
Run once: python setup_vault.py
"""

import os
import sys
from datetime import datetime, timezone

# Fix Windows console encoding for emojis
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

# ── CONFIGURE THIS ──────────────────────────────────────────────────────────
# Change this to wherever you want your Obsidian vault
VAULT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "PersonalAI_Vault")
# ─────────────────────────────────────────────────────────────────────────────

FOLDERS = ["Inbox", "Needs_Action", "Done", "Skills", "Logs"]

DASHBOARD_CONTENT = f"""# 🤖 AI Employee Dashboard
*Last updated: {datetime.now().strftime("%Y-%m-%d %H:%M")}*

---

## 📊 Today's Summary

| Metric           | Count |
|------------------|-------|
| 📥 Inbox Items   | 0     |
| ⚡ Needs Action  | 0     |
| ✅ Done Today    | 0     |

---

## 🧠 Last AI Action
> *No actions taken yet. Drop a file into /Inbox to begin.*

---

## 📋 Recent Activity Log
*(Auto-populated by agent)*

---

## 🎯 Status
**Agent:** 🟢 Online  
**Watcher:** 🟡 Not Started  
**Last Run:** Never
"""

HANDBOOK_CONTENT = """# 📖 Company Handbook — AI Employee Rules

*This file governs how the AI agent behaves. It is loaded before every action.*

---

## RULE 1 — NEVER DELETE FILES
The agent MUST NOT permanently delete any file. It may only move files between
/Inbox, /Needs_Action, and /Done folders. Deletion requires explicit human confirmation.

## RULE 2 — HUMAN APPROVAL FOR EXTERNAL ACTIONS
Before sending any email, message, or making any API call to an external service,
the agent MUST write the proposed action to /Needs_Action and WAIT for human approval.
It does NOT execute external actions autonomously.

## RULE 3 — CLASSIFY URGENCY ON EVERY ITEM
Every item processed from /Inbox must be tagged with one of:
- 🔴 URGENT — Needs human attention within 1 hour
- 🟡 NORMAL — Needs attention today
- 🟢 LOW — Can wait, informational only

## RULE 4 — ALWAYS UPDATE THE DASHBOARD
After processing any file, the agent MUST update Dashboard.md with:
- Timestamp of action
- File that was processed
- Classification assigned
- Output file created

## RULE 5 — LOG EVERYTHING
Every action, decision, and error must be appended to Logs/watcher.log
with a UTC timestamp. Logs are NEVER cleared by the agent.

## RULE 6 — STAY IN SCOPE
The agent only reads files from /Inbox. It does not browse the internet,
access other folders on the computer, or make unsolicited API calls.

## RULE 7 — STRUCTURED OUTPUT ONLY
All responses written to /Needs_Action must follow this format:
```
# Response: [original filename]
**Processed:** [timestamp]
**Urgency:** [level]
**Summary:** [2-3 sentences]
**Recommended Action:** [what the human should do]
**Raw AI Analysis:**
[full AI output]
```
"""

TRIAGE_SKILL = """# Skill: Triage Inbox Item

**Trigger:** A new file appears in /Inbox  
**Input:** Contents of the new file  
**Output:** Structured note in /Needs_Action

---

## Steps

1. Read the full contents of the inbox file
2. Read Company_Handbook.md for behavioral rules
3. Determine urgency level (URGENT / NORMAL / LOW) based on:
   - Keywords: "urgent", "ASAP", "deadline", "payment" → URGENT
   - Keywords: "meeting", "task", "follow up", "reminder" → NORMAL
   - Everything else → LOW
4. Write a 2-3 sentence summary
5. Determine recommended action for the human
6. Write output file to /Needs_Action using the format in Rule 7

## Output Template
```
# Response: {filename}
**Processed:** {timestamp}
**Urgency:** {level}
**Summary:** {summary}
**Recommended Action:** {action}

---
## Raw AI Analysis:
{full_output}
```
"""

DASHBOARD_SKILL = """# Skill: Write Dashboard

**Trigger:** After any inbox item is processed  
**Input:** Current vault stats (file counts in each folder)  
**Output:** Updated Dashboard.md

---

## Steps

1. Count files in /Inbox → inbox_count
2. Count files in /Needs_Action → action_count
3. Count files in /Done → done_count
4. Read last 3 lines of Logs/watcher.log → recent_activity
5. Get current timestamp
6. Rewrite Dashboard.md with updated numbers and activity

## Dashboard Template
```markdown
# 🤖 AI Employee Dashboard
*Last updated: {timestamp}*

## 📊 Today's Summary
| Metric          | Count        |
|-----------------|--------------|
| 📥 Inbox Items  | {inbox_count}|
| ⚡ Needs Action | {action_count}|
| ✅ Done Today   | {done_count} |

## 🧠 Last AI Action
> Processed: {last_file}
> Classification: {urgency}
> Time: {timestamp}

## 📋 Recent Activity
{recent_activity}

## 🎯 Status
**Agent:** 🟢 Online
**Last Run:** {timestamp}
```
"""

def create_vault():
    print(f"\n🚀 Creating PersonalAI_Vault at: {VAULT_PATH}\n")
    
    # Create root
    os.makedirs(VAULT_PATH, exist_ok=True)
    
    # Create subfolders
    for folder in FOLDERS:
        path = os.path.join(VAULT_PATH, folder)
        os.makedirs(path, exist_ok=True)
        print(f"  ✅ Created /{folder}")
    
    # Create files
    files = {
        "Dashboard.md": DASHBOARD_CONTENT,
        "Company_Handbook.md": HANDBOOK_CONTENT,
        "Skills/skill_triage.md": TRIAGE_SKILL,
        "Skills/skill_write_dashboard.md": DASHBOARD_SKILL,
        "Logs/watcher.log": f"[{datetime.now(timezone.utc).isoformat()}] Vault initialized.\n",
    }
    
    for filename, content in files.items():
        filepath = os.path.join(VAULT_PATH, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  ✅ Created {filename}")
    
    # Create a sample inbox item so you can test immediately
    sample = os.path.join(VAULT_PATH, "Inbox", "sample_task.txt")
    with open(sample, "w") as f:
        f.write("Urgent: Please review the project proposal document and give feedback before Friday's meeting. The client is waiting.")
    print(f"  ✅ Created Inbox/sample_task.txt (for testing)")
    
    print(f"\n✨ Vault created successfully!")
    print(f"📂 Open Obsidian → Open Folder as Vault → Select: {VAULT_PATH}")
    print(f"\nNext step: Run python watcher.py\n")

if __name__ == "__main__":
    create_vault()
