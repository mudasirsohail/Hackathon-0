# Skill: Write Dashboard

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
