# Prompt: linkedin_poster
## Date: 2026-02-19
## Purpose: Implement LinkedIn Poster that auto-posts content to LinkedIn on schedule

## Prompt Used:
Create linkedin_poster.py that:
1. Inherits from BaseWatcher
2. Uses Playwright to automate LinkedIn
3. Reads post content from Posts/ folder
4. Logs in with saved session (persistent cookies)
5. Creates posts with text and optional images
6. Tracks posted content to avoid duplicates

Requirements:
- Session saved in PersonalAI_Vault/credentials/linkedin_session/
- Support scheduled posting (daily at 9:00 AM via Task Scheduler)
- Handle image attachments with posts
- Error handling for LinkedIn UI changes
- Runs headless=False for visibility

## Result:
Created `linkedin_poster.py` with:
- LinkedInPoster class extending BaseWatcher
- Playwright browser automation with persistent context
- Post content reading from Posts/ folder (markdown files)
- Image attachment support via file upload
- Posted tracking in processed_linkedin.json

## Notes:
- Scheduled via Windows Task Scheduler (daily at 9:00 AM)
- Posts folder contains draft posts with frontmatter metadata
- Session persistence avoids repeated logins
