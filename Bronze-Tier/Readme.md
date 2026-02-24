# 🤖 Personal AI Employee — Bronze Tier
### Hackathon 0 | Governor House | Built with Qwen CLI + Obsidian

---

## What This Does

Drops a text file into a folder → AI reads it → classifies urgency → writes a structured
response → updates your Obsidian dashboard. Fully automatic. No typing required after setup.

```
You drop file.txt into /Inbox
       ↓
watcher.py detects it
       ↓
agent_runner.py reads it + Company_Handbook.md
       ↓
Qwen analyzes it using skill_triage.md
       ↓
Response written to /Needs_Action/
Dashboard.md updated
file.txt moved to /Done/
```

---

## ⚡ Quick Start (5 steps)

### Step 1 — Install dependencies

```bash
pip install watchdog requests
npm install -g @modelcontextprotocol/server-filesystem
```

### Step 2 — Create the vault

```bash
python setup_vault.py
```

Then open Obsidian → **Open folder as vault** → select `~/PersonalAI_Vault`

### Step 3 — Configure Qwen

Open `agent_runner.py` and at the top, set one of:

**Option A — Qwen CLI:**
```python
QWEN_COMMAND = ["qwen", "chat"]   # or whatever your CLI command is
USE_API = False
```

**Option B — Qwen API (Alibaba Cloud):**
```python
USE_API = True
QWEN_API_KEY = "your-key-here"   # or set env var QWEN_API_KEY
```

**Option C — Ollama (local, free):**
```python
QWEN_COMMAND = ["ollama", "run", "qwen2.5"]
USE_API = False
```

### Step 4 — Start the watcher

```bash
python watcher.py
```

Leave this running. It monitors `/Inbox` 24/7.

### Step 5 — Test it!

Drop any `.txt` file into `~/PersonalAI_Vault/Inbox/`. The agent will:
- Process it in < 30 seconds
- Write a response to `/Needs_Action/`
- Update `Dashboard.md` in Obsidian

---

## 📁 Vault Structure

```
PersonalAI_Vault/
├── Dashboard.md          ← Open this in Obsidian — your command center
├── Company_Handbook.md   ← Rules the AI follows
├── Inbox/                ← Drop files here to trigger the AI
├── Needs_Action/         ← AI responses waiting for your review
├── Done/                 ← Processed files (auto-archived)
├── Skills/
│   ├── skill_triage.md
│   └── skill_write_dashboard.md
└── Logs/
    └── watcher.log
```

---

## 🛠 Troubleshooting

| Problem | Fix |
|---------|-----|
| `watchdog` not found | `pip install watchdog` |
| Qwen CLI not found | Check `QWEN_COMMAND` in `agent_runner.py` |
| Dashboard not updating | Ensure `watcher.py` is running |
| Nothing happens on file drop | Check `Logs/watcher.log` for errors |
| MCP server won't start | Update path in `mcp_config.json` |

---

## 🏆 Bronze Tier Checklist

- [ ] Vault with Dashboard.md and Company_Handbook.md
- [ ] Working watcher script (filesystem)
- [ ] Qwen reads from vault, writes response back
- [ ] Folder structure: /Inbox, /Needs_Action, /Done
- [ ] Agent Skills documented in /Skills
- [ ] filesystem-mcp configured
- [ ] Code on GitHub

---

## 📦 Files in this Project

| File | Purpose |
|------|---------|
| `setup_vault.py` | Creates vault folders and initial files |
| `watcher.py` | Monitors /Inbox and triggers agent |
| `agent_runner.py` | Calls Qwen, writes output, updates dashboard |
| `mcp_config.json` | MCP server configuration |
| `sp.constitution.md` | Project governance rules |
| `SPEC.md` | Full feature specification |
| `PLAN.md` | Development phases |
| `TASKS.md` | Atomic task checklist |
