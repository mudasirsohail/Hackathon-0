---
id: 002
title: Watcher Implementation
stage: general
date: 2026-02-18
surface: agent
model: qwen-cli
feature: none
branch: main
user: MUDASIR SOHAIL
command: python watcher.py
labels: ["watcher","filesystem","python","bronze-tier"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - D:\Hackathon 0\Bronze-Tier\watcher.py
tests:
  - python -c "import watcher" (import test)
---

## Prompt

setup_vault.py is working. Now write watcher.py using Python watchdog that monitors ~/PersonalAI_Vault/Inbox for new .txt and .md files and calls agent_runner.py when one appears. Log everything to Logs/watcher.log

## Response snapshot

Created `watcher.py` that:
- Uses watchdog Observer to monitor Inbox folder for file creation events
- Filters for .txt and .md files only, ignores other file types
- Logs to both console and Logs/watcher.log with UTF-8 encoding
- Triggers agent_runner.py via subprocess with 2-minute timeout
- Handles errors: timeout, subprocess failures, unexpected exceptions
- Runs continuously until Ctrl+C pressed

## Outcome

- ✅ Impact: Watcher script ready to monitor inbox and trigger AI agent
- 🧪 Tests: Import test passed, watchdog library already installed (v6.0.0)
- 📁 Files: 1 Python script created (watcher.py)
- 🔁 Next prompts: Build agent_runner.py to call Qwen CLI
- 🧠 Reflection: Watchdog provides efficient native file system monitoring

## Evaluation notes (flywheel)

- Failure modes observed: None during syntax check
- Graders run and results (PASS/FAIL): PASS - imports successfully
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Build agent_runner.py with Qwen CLI integration
