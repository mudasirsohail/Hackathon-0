# 🤖 Personal AI Employee — Silver Tier
### Hackathon 0 | Governor House | Gmail + WhatsApp + LinkedIn + Approval Workflow

---

## What This Adds Over Bronze

| Feature | Bronze | Silver |
|---------|--------|--------|
| Watchers | 1 (filesystem) | 3 (filesystem + Gmail + WhatsApp) |
| AI Loop | Single triage | Reasoning + Plan.md generation |
| External Actions | None | Email sending + LinkedIn posting |
| Human Approval | Not required | Required for all external actions |
| Scheduling | Manual | Windows Task Scheduler (automatic) |

---

## ⚡ Setup Order (follow exactly)

### Step 1 — Install packages
```bash
pip install google-auth google-auth-oauthlib google-api-python-client playwright
playwright install chromium
```

### Step 2 — Extend vault
```bash
python setup_silver_vault.py
```

### Step 3 — Setup Gmail API
1. Go to console.cloud.google.com
2. Create new project → Enable Gmail API
3. Create OAuth 2.0 credentials → Desktop App
4. Download JSON → save as `PersonalAI_Vault/credentials/gmail_credentials.json`

### Step 4 — Run Gmail Watcher (first time)
```bash
python gmail_watcher.py
```
Browser opens → Login with Google → Done. Token saved automatically.

### Step 5 — Run WhatsApp Watcher (first time)
```bash
python whatsapp_watcher.py
```
Chromium opens → Scan QR code with phone → Session saved automatically.

### Step 6 — Set environment variables (for email sending)
```bash
# Windows
set SMTP_EMAIL=your@gmail.com
set SMTP_PASSWORD=your_app_password
set LINKEDIN_TOKEN=your_linkedin_token
set LINKEDIN_PERSON_ID=your_person_id
```

### Step 7 — Run Approval Handler
```bash
python approval_handler.py
```

### Step 8 — Setup Task Scheduler (run as Administrator)
```bash
python scheduler_setup.py
```

---

## How Approval Workflow Works

```
AI writes draft → /Needs_Action/APPROVAL_REQUIRED/DRAFT_xxx.md
                          ↓
         You open it in Obsidian / File Explorer
                          ↓
    Rename to APPROVED_xxx.md OR REJECTED_xxx.md
                          ↓
    approval_handler.py detects rename instantly
                          ↓
         Executes action OR archives with no action
```

---

## Running All Watchers Together

Open 3 separate terminals:

```bash
# Terminal 1
python gmail_watcher.py

# Terminal 2  
python whatsapp_watcher.py

# Terminal 3
python approval_handler.py
```

Or after Task Scheduler setup — everything runs automatically on login!

---

## Security Notes

- `credentials/` folder is blocked from GitHub via `.gitignore`
- Never share `gmail_credentials.json` or `token.json`
- Use Gmail App Passwords (not your real password) for SMTP
- LinkedIn token expires — regenerate monthly at developer.linkedin.com
