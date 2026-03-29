import os
import subprocess
from datetime import datetime, timezone

def get_recent_commits(n=5):
    try:
        result = subprocess.run(
            ["git", "log", f"-{n}", "--pretty=format:%s (%ar)"],
            capture_output=True, text=True
        )
        return result.stdout.strip().split("\n") if result.stdout.strip() else []
    except Exception:
        return []

def get_repo_files():
    ignore = {'.git', '__pycache__', '.github', 'node_modules'}
    files = []
    for root, dirs, filenames in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in ignore]
        for f in filenames:
            path = os.path.join(root, f).lstrip('./')
            if path:
                files.append(path)
    return sorted(files)

def generate():
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    commits = get_recent_commits()
    files = get_repo_files()

    commit_lines = "\n".join(f"- {c}" for c in commits) if commits else "- No commits found"
    file_lines = "\n".join(f"- `{f}`" for f in files) if files else "- No files found"

    readme = f"""# 👋 Rajesh Kumar Jogi

> Auto-generated on {now}

## 🗂️ Repository Files

{file_lines}

## 📝 Recent Activity

{commit_lines}

---
*This README is automatically updated daily via GitHub Actions.*
"""

    # with open("README.md", "w") as f:
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme)
    print("✅ README.md generated successfully.")

if __name__ == "__main__":
    generate()