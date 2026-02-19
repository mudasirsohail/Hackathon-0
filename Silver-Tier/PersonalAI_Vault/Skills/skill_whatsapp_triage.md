# Skill: WhatsApp Message Triage

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
