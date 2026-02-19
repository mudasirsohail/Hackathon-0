# Skill: Gmail Reply Drafter

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
