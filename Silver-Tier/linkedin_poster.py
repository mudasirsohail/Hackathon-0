"""
linkedin_poster.py — Generates a LinkedIn post using Qwen and sends it for approval.
Run manually or via Task Scheduler daily at 9am.
"""

import os
import subprocess
from pathlib import Path
from datetime import datetime

VAULT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "PersonalAI_Vault")
APPROVAL_PATH = os.path.join(VAULT_PATH, "Needs_Action", "APPROVAL_REQUIRED")
DONE_PATH = os.path.join(VAULT_PATH, "Done")
LINKEDIN_SESSION_PATH = os.path.join(VAULT_PATH, "credentials", "linkedin_session")


def read_file(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except:
        return ""


def call_qwen(prompt: str) -> str:
    """Calls Qwen CLI and returns response."""
    try:
        result = subprocess.run(
            "qwen chat",
            input=prompt,
            capture_output=True,
            text=True,
            timeout=90,
            shell=True,
            encoding="utf-8",
            errors="replace"
        )
        return result.stdout.strip()
    except Exception as e:
        return f"[ERROR] {e}"


def get_recent_activity() -> str:
    """Reads last 3 Done files to understand recent completions."""
    done_dir = Path(DONE_PATH)
    files = sorted(done_dir.iterdir(), key=lambda x: x.stat().st_mtime, reverse=True)[:3]
    summaries = []
    for f in files:
        if f.suffix in [".txt", ".md"]:
            content = f.read_text(encoding="utf-8", errors="replace")
            summaries.append(f"- {f.name}: {content[:200]}")
    return "\n".join(summaries) if summaries else "No recent activity found."


def generate_linkedin_post() -> str:
    prompt = """Write a LinkedIn post about this achievement.
    
Topic: Completed Silver Tier of Hackathon 0 at Governor House

What was built:
- Gmail Watcher monitors important emails automatically 24/7
- WhatsApp Watcher detects urgent keyword messages in real time
- Email sending system with human-in-the-loop approval workflow
- LinkedIn auto-posting powered by Qwen AI
- Approval Handler executes actions after human review
- Windows Task Scheduler runs everything automatically

Tech stack: Python, Qwen CLI, Playwright, Gmail API, Obsidian

Rules:
- Do NOT mention Ramadan
- Do NOT mention emails sent to anyone
- ONLY talk about the hackathon achievement
- Sound human and genuine
- 150-200 words
- End with these hashtags only:
  #Hackathon0 #GovernorHouse #AIAgent #Python #Qwen #BuildInPublic

Write ONLY the post. Nothing else."""

    return call_qwen(prompt)


def post_via_playwright(content: str) -> bool:
    from playwright.sync_api import sync_playwright
    import time
    
    SESSION_PATH = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "PersonalAI_Vault", "credentials", "linkedin_session"
    )
    os.makedirs(SESSION_PATH, exist_ok=True)
    
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            SESSION_PATH,
            headless=False,
            viewport={"width": 1280, "height": 800}
        )
        page = browser.pages[0] if browser.pages else browser.new_page()
        page.goto("https://www.linkedin.com/feed/", timeout=60000)
        
        print("Waiting for LinkedIn feed...")
        page.wait_for_timeout(5000)
        
        # Try multiple selectors for Start a post button
        post_selectors = [
            'button[aria-label="Start a post"]',
            '.share-box-feed-entry__trigger',
            'button.share-box-feed-entry__trigger',
            '[data-testid="share-box-feed-entry__trigger"]',
            'div.share-box-feed-entry__top-bar button',
        ]
        
        clicked = False
        for selector in post_selectors:
            try:
                btn = page.wait_for_selector(selector, timeout=5000)
                if btn:
                    btn.click()
                    print(f"Clicked post button: {selector}")
                    clicked = True
                    break
            except:
                continue
        
        if not clicked:
            # Try JavaScript click as last resort
            try:
                page.evaluate("""
                    const buttons = document.querySelectorAll('button');
                    for(const btn of buttons) {
                        if(btn.innerText.includes('Start a post') || 
                           btn.innerText.includes('Write an article')) {
                            btn.click();
                            break;
                        }
                    }
                """)
                clicked = True
                print("Clicked via JavaScript")
            except:
                pass
        
        if not clicked:
            print("Could not find post button. Is LinkedIn logged in?")
            browser.close()
            return False
        
        page.wait_for_timeout(3000)
        
        # Type content in post box
        editor_selectors = [
            'div[role="textbox"]',
            '.ql-editor',
            'div[contenteditable="true"]',
        ]
        
        for selector in editor_selectors:
            try:
                editor = page.wait_for_selector(selector, timeout=5000)
                if editor:
                    editor.click()
                    page.keyboard.type(content)
                    print("Content typed successfully")
                    break
            except:
                continue
        
        page.wait_for_timeout(2000)
        
        # Click Post button
        submit_selectors = [
            'button[aria-label="Post"]',
            '.share-actions__primary-action',
            'button.share-actions__primary-action',
        ]
        
        for selector in submit_selectors:
            try:
                btn = page.wait_for_selector(selector, timeout=5000)
                if btn:
                    btn.click()
                    print("Post submitted!")
                    break
            except:
                continue
        
        page.wait_for_timeout(3000)
        browser.close()
        return True


def save_for_approval(post_content: str):
    """Saves the draft post to APPROVAL_REQUIRED folder."""
    date_str = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"LINKEDIN_POST_{date_str}.md"
    filepath = os.path.join(APPROVAL_PATH, filename)

    content = f"""# 💼 LinkedIn Post Draft — Awaiting Approval
**Created:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Action:** LINKEDIN_POST

---

## Post Content:
{post_content}

---

## Instructions:
✅ To POST: Rename this file to → `APPROVED_{filename}`
❌ To SKIP: Rename this file to → `REJECTED_{filename}`

The approval_handler.py will detect the rename and act automatically.
"""

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"\n✅ LinkedIn post draft saved!")
    print(f"📂 Open this file in Obsidian or File Explorer:")
    print(f"   {filepath}")
    print(f"\n👆 Rename to APPROVED_{filename} to post it")
    print(f"   Rename to REJECTED_{filename} to skip it\n")


def main():
    print("=" * 50)
    print("🚀 LinkedIn Poster starting...")
    print("=" * 50)
    post = generate_linkedin_post()

    if "[ERROR]" in post:
        print(f"❌ Qwen failed: {post}")
        return

    print(f"\n📝 Generated Post Preview:\n")
    print("-" * 40)
    print(post)
    print("-" * 40)

    save_for_approval(post)


if __name__ == "__main__":
    main()
