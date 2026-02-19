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
    """Uses Qwen to generate a professional LinkedIn post."""
    skill = read_file(os.path.join(VAULT_PATH, "Skills", "skill_linkedin_post.md"))
    recent = get_recent_activity()
    dashboard = read_file(os.path.join(VAULT_PATH, "Dashboard.md"))

    prompt = f"""You are a Personal AI Employee writing a LinkedIn post for your employer's business.

=== LINKEDIN POST SKILL ===
{skill}

=== RECENT COMPLETED WORK ===
{recent}

=== DASHBOARD SUMMARY ===
{dashboard}

=== YOUR TASK ===
Write ONE compelling LinkedIn post about the work being done, a business insight,
or a lesson learned. Follow the skill instructions exactly. Make it sound genuine
and human — not like AI wrote it. 150-300 words. Include 3-5 hashtags at the end.

Write ONLY the post content. No preamble, no explanation.
"""

    print("🧠 Qwen generating LinkedIn post...")
    return call_qwen(prompt)


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
