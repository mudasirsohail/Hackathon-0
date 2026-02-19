# Skill: Triage Inbox Item

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
