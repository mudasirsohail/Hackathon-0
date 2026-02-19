# PLAN.md — Silver Tier Development Plan
## Estimated Time: 20-30 hours across sessions

---

## PHASE 1 — SETUP & CREDENTIALS (2-3 hours)
*Get all new tools and API access ready before writing code.*

- [ ] Copy Bronze-Tier vault into Silver-Tier folder
- [ ] Install new Python packages:
      pip install google-auth google-auth-oauthlib google-api-python-client playwright
- [ ] Install Playwright browsers: playwright install chromium
- [ ] Create Google Cloud project and enable Gmail API
- [ ] Download gmail_credentials.json from Google Cloud Console
- [ ] Create credentials/ folder with .gitignore
- [ ] Create LinkedIn Developer App and get access token
- [ ] Install email-mcp: npm install -g email-mcp (or configure smtplib)
- [ ] Test Gmail API connection manually

---

## PHASE 2 — BASE WATCHER & VAULT EXTENSION (2 hours)
*Build the foundation all watchers share.*

- [ ] Write base_watcher.py with abstract BaseWatcher class
- [ ] Extend vault: add /Plans and /Needs_Action/APPROVAL_REQUIRED folders
- [ ] Write setup_silver_vault.py to add new folders and skill files
- [ ] Run setup_silver_vault.py and verify in Obsidian
- [ ] Write 4 new Skill markdown files
- [ ] Commit: "feat: silver vault structure"

---

## PHASE 3 — GMAIL WATCHER (4-5 hours)
*Connect to Gmail and pull important unread emails.*

- [ ] Write gmail_watcher.py inheriting BaseWatcher
- [ ] Implement OAuth2 login flow (first run opens browser)
- [ ] Implement check_for_updates() — fetch unread+important emails
- [ ] Implement create_action_file() — write structured .md to /Needs_Action
- [ ] Test: send yourself an email marked important, verify .md appears
- [ ] Add processed_ids tracking so no duplicate processing
- [ ] Connect to agent_runner.py so Qwen analyzes each email
- [ ] Commit: "feat: gmail watcher working"

---

## PHASE 4 — WHATSAPP WATCHER (4-5 hours)
*Automate WhatsApp Web to detect keyword messages.*

- [ ] Write whatsapp_watcher.py inheriting BaseWatcher
- [ ] Implement Playwright browser launch with persistent session
- [ ] First run: open browser, scan QR code, session saved
- [ ] Implement keyword detection on unread chats
- [ ] Implement create_action_file() for WhatsApp messages
- [ ] Test: send yourself a WhatsApp message with "urgent", verify .md appears
- [ ] Commit: "feat: whatsapp watcher working"

---

## PHASE 5 — AI REASONING LOOP & PLAN.MD (3-4 hours)
*Upgrade agent to generate plans, not just triage.*

- [ ] Upgrade agent_runner.py with reasoning loop
- [ ] Implement: read ALL /Needs_Action files, not just one
- [ ] Implement: generate Plan.md with priorities and next actions
- [ ] Implement: save Plan.md to /Plans/ with timestamp
- [ ] Test: have 3 items in Needs_Action, verify Plan.md is generated
- [ ] Commit: "feat: reasoning loop with plan generation"

---

## PHASE 6 — HUMAN APPROVAL WORKFLOW (3 hours)
*Build the approval system for sensitive actions.*

- [ ] Write approval_handler.py
- [ ] Implement: monitor /APPROVAL_REQUIRED/ for file renames
- [ ] Implement: parse action type from file (email / linkedin / whatsapp)
- [ ] Implement: execute approved action
- [ ] Implement: move to /Done after execution
- [ ] Test full loop: AI drafts → human approves → action executes
- [ ] Commit: "feat: human approval workflow"

---

## PHASE 7 — EMAIL MCP + LINKEDIN POSTER (3-4 hours)
*Wire up external actions with approval gate.*

- [ ] Configure email-mcp server
- [ ] Write email draft skill — Qwen drafts reply, saves to APPROVAL_REQUIRED
- [ ] Test email sending after approval
- [ ] Write linkedin_poster.py
- [ ] Qwen generates post → saved to APPROVAL_REQUIRED → approved → posted
- [ ] Test LinkedIn post end to end
- [ ] Commit: "feat: email mcp and linkedin poster"

---

## PHASE 8 — TASK SCHEDULER (1-2 hours)
*Make everything run automatically on Windows.*

- [ ] Write scheduler_setup.py
- [ ] Register Gmail Watcher task (every 2 min)
- [ ] Register WhatsApp Watcher task (every 30 sec)
- [ ] Register Dashboard update task (every 5 min)
- [ ] Register LinkedIn post task (daily 9am)
- [ ] Test: restart computer, verify tasks run automatically
- [ ] Commit: "feat: windows task scheduler configured"

---

## PHASE 9 — POLISH & DEMO (1-2 hours)
- [ ] Verify all 8 Acceptance Criteria pass
- [ ] Update README with Silver Tier setup guide
- [ ] Ensure credentials/ is NOT in GitHub
- [ ] Final commit and push
- [ ] Record demo video

---

## RISK LOG

| Risk                              | Mitigation                                    |
|-----------------------------------|-----------------------------------------------|
| WhatsApp blocks automation        | Use persistent session, avoid rapid requests  |
| Gmail OAuth refresh token expires | Implement auto-refresh in gmail_watcher.py    |
| LinkedIn API rate limits          | Max 1 post per day, human approval required   |
| Task Scheduler permissions        | Run as Administrator when setting up          |
