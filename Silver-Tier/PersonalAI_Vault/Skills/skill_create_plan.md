# Skill: Create Daily Plan

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
