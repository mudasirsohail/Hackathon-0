# Prompt: scheduler
## Date: 2026-02-19
## Purpose: Create Windows Task Scheduler setup script for all Silver Tier watchers

## Prompt Used:
Create scheduler_setup.py that:
1. Registers all 4 watchers with Windows Task Scheduler
2. Configures appropriate schedules for each watcher:
   - Gmail Watcher: every 2 minutes (on logon + repeat)
   - WhatsApp Watcher: every 2 minutes (on logon + repeat)
   - Approval Handler: every 30 seconds (on logon + repeat)
   - LinkedIn Poster: daily at 9:00 AM
3. Handles path escaping for spaces in directory names
4. Runs once as Administrator to set up all tasks
5. Provides verification commands and cleanup instructions

Requirements:
- Use schtasks command-line tool
- Wrap paths in escaped quotes for spaces (e.g., "MUDASIR SOHAIL", "Hackathon 0")
- Force overwrite existing tasks (/f flag)
- Display success/failure for each task
- Include helpful output for verification and management

## Result:
Created `scheduler_setup.py` with:
- create_task() function with proper path escaping (\\" for schtasks)
- Task configuration for all 4 watchers
- Username detection via os.environ.get("USERNAME")
- Clear console output with emoji indicators
- Verification instructions for Task Scheduler GUI

## Notes:
- Fixed path escaping issue: paths with spaces now wrapped in escaped quotes
- Command format: schtasks /create /tn "name" /tr "\"python.exe\" \"script.py\"" /sc onlogon /f
- Must run as Administrator for task creation
