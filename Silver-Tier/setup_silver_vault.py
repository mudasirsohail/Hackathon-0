"""
setup_silver_vault.py — Extends the Bronze vault with Silver Tier folders and skills.
Run once: python setup_silver_vault.py
"""

import os
from datetime import datetime

VAULT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "PersonalAI_Vault")

NEW_FOLDERS = [
    "Plans",
    os.path.join("Needs_Action", "APPROVAL_REQUIRED"),
    "credentials"
]

SKILL_GMAIL = """# Skill: Gmail Reply Drafter

**Trigger:** A new EMAIL_xxx.md file appears in /Needs_Action
**Input:** Email sender, subject, and snippet content
**Output:** Draft reply saved to /Needs_Action/APPROVAL_REQUIRED/

---

## Steps

1. Read the email .md file from /Needs_Action
2. Identify the sender's request or question
3. Draft a professional, concise reply using Qwen
4. Determine tone: formal (business) or friendly (personal)
5. Write draft to /Needs_Action/APPROVAL_REQUIRED/DRAFT_EMAIL_{id}.md
6. Include: To, Subject, Body, and the send command

## Output Template
```
# EMAIL DRAFT — Awaiting Approval
**To:** {sender_email}
**Subject:** Re: {original_subject}
**Action:** SEND_EMAIL
**Created:** {timestamp}

---

## Draft Body:
{qwen_generated_reply}

---

## To Approve: Rename this file to APPROVED_DRAFT_EMAIL_{id}.md
## To Reject: Rename this file to REJECTED_DRAFT_EMAIL_{id}.md
```
"""

SKILL_WHATSAPP = """# Skill: WhatsApp Message Triage

**Trigger:** A new WHATSAPP_xxx.md file appears in /Needs_Action
**Input:** WhatsApp message text and sender
**Output:** Classification + recommended action

---

## Steps

1. Read the WhatsApp .md file
2. Identify which keyword triggered it: urgent/asap/invoice/payment/help/deadline/meeting
3. Classify urgency:
   - "invoice" or "payment" → 🔴 URGENT (money involved)
   - "urgent" or "asap" or "deadline" → 🔴 URGENT
   - "help" or "meeting" → 🟡 NORMAL
4. Draft a suggested reply (short, WhatsApp-appropriate)
5. Write suggested reply to APPROVAL_REQUIRED if reply is needed
6. Update Dashboard.md

## Output Template
```
# WhatsApp Alert
**From:** {sender}
**Keyword Triggered:** {keyword}
**Urgency:** {level}
**Message:** {content}
**Suggested Reply:** {draft}
**Action Required:** {what human should do}
```
"""

SKILL_LINKEDIN = """# Skill: LinkedIn Business Post Writer

**Trigger:** Daily at 9am via Task Scheduler OR manual trigger
**Input:** Recent activity, completed tasks, business updates from vault
**Output:** Draft LinkedIn post in /Needs_Action/APPROVAL_REQUIRED/

---

## Steps

1. Read Dashboard.md to understand recent activity
2. Read last 3 items in /Done to find completed work
3. Identify a business insight, win, or lesson to share
4. Write a LinkedIn post that:
   - Starts with a hook (question or bold statement)
   - Shares a genuine insight or result
   - Ends with a call to action or question
   - Uses 3-5 relevant hashtags
   - Is 150-300 words
   - Sounds human, not robotic
5. Save to /Needs_Action/APPROVAL_REQUIRED/LINKEDIN_POST_{date}.md

## Post Formula
```
[HOOK — bold first line]

[STORY or INSIGHT — 2-3 short paragraphs]

[LESSON or RESULT]

[CALL TO ACTION or QUESTION]

#hashtag1 #hashtag2 #hashtag3
```
"""

SKILL_PLAN = """# Skill: Create Daily Plan

**Trigger:** After processing multiple Needs_Action items OR daily at 8am
**Input:** All files currently in /Needs_Action
**Output:** Plan.md saved to /Plans/

---

## Steps

1. List all files in /Needs_Action (excluding APPROVAL_REQUIRED subfolder)
2. For each file, extract: urgency level, type, recommended action
3. Sort by urgency: URGENT first, then NORMAL, then LOW
4. Estimate time for each: URGENT=30min, NORMAL=15min, LOW=5min
5. Group by type: Emails, WhatsApp, Tasks, Other
6. Generate Plan.md with prioritized action list
7. Save to /Plans/Plan_{timestamp}.md
8. Update Dashboard.md with today's plan summary

## Plan.md Template
```markdown
# 📋 Daily Action Plan
**Generated:** {timestamp}
**Total Items:** {count}
**Estimated Time:** {total_minutes} minutes

---

## 🔴 URGENT ({urgent_count} items)
{urgent_items}

## 🟡 NORMAL ({normal_count} items)
{normal_items}

## 🟢 LOW ({low_count} items)
{low_items}

---

## Summary
{qwen_summary_of_day}
```
"""

GITIGNORE_CONTENT = """# Block credentials from GitHub — CRITICAL SECURITY
*
!.gitignore
"""

def setup_silver():
    print(f"\n🚀 Extending vault for Silver Tier at: {VAULT_PATH}\n")

    if not os.path.exists(VAULT_PATH):
        print("❌ Bronze vault not found! Run setup_vault.py first.")
        return

    # Create new folders
    for folder in NEW_FOLDERS:
        path = os.path.join(VAULT_PATH, folder)
        os.makedirs(path, exist_ok=True)
        print(f"  ✅ Created /{folder}")

    # Create credentials .gitignore
    gitignore_path = os.path.join(VAULT_PATH, "credentials", ".gitignore")
    with open(gitignore_path, "w") as f:
        f.write(GITIGNORE_CONTENT)
    print(f"  ✅ Created credentials/.gitignore (blocks secrets from GitHub)")

    # Also create .gitignore at Silver-Tier root level
    root_gitignore = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".gitignore")
    with open(root_gitignore, "w") as f:
        f.write("""# Silver Tier .gitignore
PersonalAI_Vault/credentials/
PersonalAI_Vault/Logs/
*.pyc
__pycache__/
token.json
whatsapp_session/
.env
""")
    print(f"  ✅ Created .gitignore at project root")

    # Write new skill files
    skills = {
        "Skills/skill_gmail_reply.md": SKILL_GMAIL,
        "Skills/skill_whatsapp_triage.md": SKILL_WHATSAPP,
        "Skills/skill_linkedin_post.md": SKILL_LINKEDIN,
        "Skills/skill_create_plan.md": SKILL_PLAN,
    }

    for filename, content in skills.items():
        filepath = os.path.join(VAULT_PATH, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  ✅ Created {filename}")

    print(f"\n✨ Silver Tier vault ready!")
    print(f"\nNext step: python base_watcher.py (to verify it imports cleanly)")

if __name__ == "__main__":
    setup_silver()
