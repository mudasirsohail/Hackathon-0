# Prompt: spec
## Date: 2026-02-19
## Purpose: Create the specification document (SPEC.md) defining functional requirements for Silver Tier

## Prompt Used:
Create a detailed specification document for Personal AI Assistant Silver Tier.

The system must include:
1. Gmail Watcher - Monitor inbox for emails with trigger keywords
2. WhatsApp Watcher - Monitor WhatsApp Web for messages with trigger keywords  
3. Approval Handler - Process user approvals for AI actions
4. LinkedIn Poster - Auto-post content to LinkedIn on schedule

Requirements:
- All watchers run on Windows Task Scheduler
- Sessions persist across restarts (no re-authentication needed)
- Trigger keywords create action files in Needs_Action folder
- Approval system with approve/reject/pending states
- LinkedIn posting with image support and scheduling

Document functional requirements, user stories, acceptance criteria, and out-of-scope items.

## Result:
Created `specs/silver-tier/spec.md` with:
- Feature breakdown for all 4 watchers
- User stories with acceptance criteria
- Data flow diagrams for message processing
- Integration points (Gmail API, WhatsApp Web, LinkedIn API)
- Out-of-scope items clearly defined (mobile apps, web UI, real-time sync)

## Notes:
- Specification focuses on automation and minimal user intervention
- Emphasis on "set and forget" operation model
- Action files use markdown format for easy human readability
