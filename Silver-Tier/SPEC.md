# SPEC.md — Silver Tier Specification
## Version: 1.0 | Status: APPROVED

---

## 1. OVERVIEW

Silver Tier extends Bronze into a real autonomous business assistant.
It watches Gmail and WhatsApp 24/7, generates reasoning plans, posts on
LinkedIn automatically (with approval), and can send emails via MCP.

---

## 2. FUNCTIONAL REQUIREMENTS

### FR-01 — Base Watcher Class
- SHALL define a `BaseWatcher` abstract class all watchers inherit from
- SHALL have: `check_for_updates()` and `create_action_file()` methods
- SHALL run in a continuous loop with configurable check interval
- SHALL log all activity to its own log file

### FR-02 — Gmail Watcher
- SHALL connect to Gmail using Google OAuth2 credentials
- SHALL check for unread + important emails every 2 minutes
- SHALL extract: sender, subject, snippet, timestamp
- SHALL create a structured .md file in /Needs_Action for each email
- SHALL NOT process the same email twice (track processed IDs)
- SHALL mark emails as read after processing

### FR-03 — WhatsApp Watcher
- SHALL use Playwright to automate WhatsApp Web
- SHALL check for unread messages every 30 seconds
- SHALL only trigger on messages containing keywords:
  urgent, asap, invoice, payment, help, deadline, meeting
- SHALL create a structured .md file in /Needs_Action for keyword messages
- SHALL save WhatsApp session so login is only needed once

### FR-04 — LinkedIn Auto-Poster
- SHALL generate a business-related LinkedIn post using Qwen
- SHALL write draft post to /Needs_Action/APPROVAL_REQUIRED/
- SHALL wait for human APPROVED_ rename before posting
- SHALL post via LinkedIn API or Playwright automation
- SHALL log every post attempt and result

### FR-05 — AI Reasoning Loop with Plan.md
- SHALL read all items in /Needs_Action
- SHALL generate a Plan.md file with:
  - Summary of all pending items
  - Prioritized action list
  - Estimated time per action
  - Dependencies between tasks
- SHALL save Plan.md to /Plans/ folder with timestamp
- SHALL update Dashboard.md with plan summary

### FR-06 — Email Sending via MCP
- SHALL use email-mcp server to send emails
- SHALL NEVER send without human approval
- SHALL write draft to /Needs_Action/APPROVAL_REQUIRED/DRAFT_EMAIL_xxx.md
- Approval file SHALL contain: To, Subject, Body, Send command
- After APPROVED_ rename, SHALL execute send via MCP

### FR-07 — Human-in-the-Loop Approval Workflow
- approval_handler.py SHALL monitor /Needs_Action/APPROVAL_REQUIRED/
- SHALL detect when human renames file to APPROVED_xxx.md
- SHALL parse the action from the file and execute it
- SHALL move executed file to /Done/
- SHALL log: what was approved, when, what action was taken

### FR-08 — Windows Task Scheduler Integration
- scheduler_setup.py SHALL register these scheduled tasks:
  - Gmail Watcher: runs every 2 minutes
  - WhatsApp Watcher: runs every 30 seconds
  - Dashboard Update: runs every 5 minutes
  - LinkedIn Post: runs every day at 9am

### FR-09 — New Agent Skills
- skill_gmail_reply.md — how to draft email replies
- skill_whatsapp_triage.md — how to classify WhatsApp messages
- skill_linkedin_post.md — how to write LinkedIn business posts
- skill_create_plan.md — how to generate Plan.md from pending items

---

## 3. NON-FUNCTIONAL REQUIREMENTS

| ID     | Requirement                                      |
|--------|--------------------------------------------------|
| NFR-01 | Gmail credentials never stored in plain text     |
| NFR-02 | WhatsApp session persists between restarts       |
| NFR-03 | All watchers run independently, failures isolated|
| NFR-04 | Approval workflow response time < 5 seconds      |
| NFR-05 | LinkedIn posts sound human, not robotic          |

---

## 4. ACCEPTANCE CRITERIA

| ID    | Criteria                                                        |
|-------|-----------------------------------------------------------------|
| AC-01 | Gmail Watcher creates .md file for each unread important email  |
| AC-02 | WhatsApp Watcher triggers on keyword message                    |
| AC-03 | LinkedIn draft appears in APPROVAL_REQUIRED folder              |
| AC-04 | Renaming to APPROVED_ triggers the actual post                  |
| AC-05 | Plan.md generated with all pending items prioritized            |
| AC-06 | Email sent only after APPROVED_ rename                          |
| AC-07 | Task Scheduler runs Gmail watcher automatically                 |
| AC-08 | credentials/ folder absent from GitHub                          |
