# TASKS.md — Silver Tier Atomic Tasks
## Status: ⬜ Todo | 🔄 In Progress | ✅ Done | ❌ Blocked

---

## GROUP 1: SETUP & CREDENTIALS

| ID    | Task                                                        | Status |
|-------|-------------------------------------------------------------|--------|
| ST-01 | pip install google-auth google-auth-oauthlib google-api-python-client | ⬜ |
| ST-02 | pip install playwright && playwright install chromium        | ⬜     |
| ST-03 | Create Google Cloud project at console.cloud.google.com     | ⬜     |
| ST-04 | Enable Gmail API in Google Cloud Console                    | ⬜     |
| ST-05 | Create OAuth credentials, download gmail_credentials.json   | ⬜     |
| ST-06 | Create credentials/ folder inside Silver-Tier               | ⬜     |
| ST-07 | Create credentials/.gitignore to block folder from GitHub   | ⬜     |
| ST-08 | Create LinkedIn Developer App at developer.linkedin.com     | ⬜     |
| ST-09 | Get LinkedIn access token                                   | ⬜     |
| ST-10 | npm install -g @modelcontextprotocol/server-filesystem       | ⬜     |

---

## GROUP 2: VAULT EXTENSION

| ID    | Task                                                        | Status |
|-------|-------------------------------------------------------------|--------|
| ST-11 | Run setup_silver_vault.py to add new folders                | ⬜     |
| ST-12 | Verify /Plans folder created                                | ⬜     |
| ST-13 | Verify /Needs_Action/APPROVAL_REQUIRED folder created       | ⬜     |
| ST-14 | Write skill_gmail_reply.md                                  | ⬜     |
| ST-15 | Write skill_whatsapp_triage.md                              | ⬜     |
| ST-16 | Write skill_linkedin_post.md                                | ⬜     |
| ST-17 | Write skill_create_plan.md                                  | ⬜     |
| ST-18 | Open vault in Obsidian, verify new folders render           | ⬜     |
| ST-19 | Git commit: "feat: silver vault structure"                  | ⬜     |

---

## GROUP 3: BASE WATCHER

| ID    | Task                                                        | Status |
|-------|-------------------------------------------------------------|--------|
| ST-20 | Write base_watcher.py with BaseWatcher abstract class       | ⬜     |
| ST-21 | Test: import BaseWatcher in Python, no errors               | ⬜     |
| ST-22 | Git commit: "feat: base watcher class"                      | ⬜     |

---

## GROUP 4: GMAIL WATCHER

| ID    | Task                                                        | Status |
|-------|-------------------------------------------------------------|--------|
| ST-23 | Write gmail_watcher.py                                      | ⬜     |
| ST-24 | Run first time: browser opens for Google login              | ⬜     |
| ST-25 | Complete OAuth login, token.json saved                      | ⬜     |
| ST-26 | Send test email to yourself marked Important                | ⬜     |
| ST-27 | Verify .md file created in /Needs_Action                    | ⬜     |
| ST-28 | Verify no duplicate processing on second run                | ⬜     |
| ST-29 | Git commit: "feat: gmail watcher"                           | ⬜     |

---

## GROUP 5: WHATSAPP WATCHER

| ID    | Task                                                        | Status |
|-------|-------------------------------------------------------------|--------|
| ST-30 | Write whatsapp_watcher.py                                   | ⬜     |
| ST-31 | First run: Chromium opens WhatsApp Web                      | ⬜     |
| ST-32 | Scan QR code with phone                                     | ⬜     |
| ST-33 | Session saved to credentials/whatsapp_session/              | ⬜     |
| ST-34 | Send yourself WhatsApp message with "urgent"                | ⬜     |
| ST-35 | Verify .md file created in /Needs_Action                    | ⬜     |
| ST-36 | Git commit: "feat: whatsapp watcher"                        | ⬜     |

---

## GROUP 6: REASONING LOOP & PLAN.MD

| ID    | Task                                                        | Status |
|-------|-------------------------------------------------------------|--------|
| ST-37 | Upgrade agent_runner.py with reasoning loop                 | ⬜     |
| ST-38 | Implement: read all /Needs_Action files                     | ⬜     |
| ST-39 | Implement: generate Plan.md via Qwen                        | ⬜     |
| ST-40 | Implement: save Plan.md to /Plans/ with timestamp           | ⬜     |
| ST-41 | Test with 3 items in Needs_Action                           | ⬜     |
| ST-42 | Git commit: "feat: reasoning loop"                          | ⬜     |

---

## GROUP 7: APPROVAL WORKFLOW

| ID    | Task                                                        | Status |
|-------|-------------------------------------------------------------|--------|
| ST-43 | Write approval_handler.py                                   | ⬜     |
| ST-44 | Test: AI writes draft to APPROVAL_REQUIRED/                 | ⬜     |
| ST-45 | Test: rename to APPROVED_ → action executes                 | ⬜     |
| ST-46 | Test: rename to REJECTED_ → file archived, no action        | ⬜     |
| ST-47 | Git commit: "feat: approval workflow"                       | ⬜     |

---

## GROUP 8: EMAIL MCP + LINKEDIN

| ID    | Task                                                        | Status |
|-------|-------------------------------------------------------------|--------|
| ST-48 | Configure email sending (smtplib or email-mcp)              | ⬜     |
| ST-49 | Test: Qwen drafts email reply → APPROVAL_REQUIRED           | ⬜     |
| ST-50 | Test: approve → email actually sent                         | ⬜     |
| ST-51 | Write linkedin_poster.py                                    | ⬜     |
| ST-52 | Test: Qwen writes LinkedIn post → APPROVAL_REQUIRED         | ⬜     |
| ST-53 | Test: approve → post appears on LinkedIn                    | ⬜     |
| ST-54 | Git commit: "feat: email and linkedin"                      | ⬜     |

---

## GROUP 9: TASK SCHEDULER

| ID    | Task                                                        | Status |
|-------|-------------------------------------------------------------|--------|
| ST-55 | Write scheduler_setup.py                                    | ⬜     |
| ST-56 | Run as Administrator: python scheduler_setup.py             | ⬜     |
| ST-57 | Verify tasks appear in Windows Task Scheduler               | ⬜     |
| ST-58 | Restart computer, verify watchers start automatically       | ⬜     |
| ST-59 | Git commit: "feat: task scheduler"                          | ⬜     |

---

## GROUP 10: FINAL

| ID    | Task                                                        | Status |
|-------|-------------------------------------------------------------|--------|
| ST-60 | Verify all 8 Acceptance Criteria from SPEC.md               | ⬜     |
| ST-61 | Confirm credentials/ not in GitHub                          | ⬜     |
| ST-62 | Update README.md for Silver Tier                            | ⬜     |
| ST-63 | Final git push                                              | ⬜     |
