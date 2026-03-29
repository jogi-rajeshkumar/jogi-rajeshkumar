"""
generate_readme.py
Auto-generates a creative, rich README.md for jogi-rajeshkumar's GitHub profile.
Run locally or via GitHub Actions daily.
"""

import urllib.request
import json
import os
from datetime import datetime, timezone

GITHUB_USERNAME = "jogi-rajeshkumar"

# ── GitHub Stats Cards ────────────────────────────────────────────────────────

def github_stats_card():
    return f"![GitHub Stats](https://github-readme-stats.vercel.app/api?username={GITHUB_USERNAME}&show_icons=true&theme=tokyonight&hide_border=true&count_private=true&include_all_commits=true)"

def github_streak():
    return f"![GitHub Streak](https://streak-stats.demolab.com?user={GITHUB_USERNAME}&theme=tokyonight&hide_border=true)"

def top_langs_card():
    return f"![Top Languages](https://github-readme-stats.vercel.app/api/top-langs/?username={GITHUB_USERNAME}&layout=compact&theme=tokyonight&hide_border=true&langs_count=8)"

def activity_graph():
    return f"![Activity Graph](https://github-readme-activity-graph.vercel.app/graph?username={GITHUB_USERNAME}&theme=tokyo-night&hide_border=true&area=true)"

def profile_trophy():
    return f"![Trophy](https://github-profile-trophy.vercel.app/?username={GITHUB_USERNAME}&theme=tokyonight&no-frame=true&row=1&column=7)"

# ── Skill Badges ──────────────────────────────────────────────────────────────

def badges():
    badge_list = [
        # Languages
        ("Python",         "3776AB", "python",              "white"),
        ("JavaScript",     "F7DF1E", "javascript",          "black"),
        ("SQL",            "4479A1", "mysql",               "white"),
        ("HTML5",          "E34F26", "html5",               "white"),
        ("CSS3",           "1572B6", "css3",                "white"),
        # AI/ML
        ("PyTorch",        "EE4C2C", "pytorch",             "white"),
        ("TensorFlow",     "FF6F00", "tensorflow",          "white"),
        ("Keras",          "D00000", "keras",               "white"),
        ("OpenCV",         "5C3EE8", "opencv",              "white"),
        ("HuggingFace",    "FFD21E", "huggingface",         "black"),
        ("scikit--learn",  "F7931E", "scikitlearn",         "white"),
        # Cloud & DevOps
        ("AWS",            "232F3E", "amazonwebservices",   "white"),
        ("Docker",         "2496ED", "docker",              "white"),
        ("GitHub%20Actions","2088FF","githubactions",       "white"),
        ("Linux",          "FCC624", "linux",               "black"),
        # Web
        ("Django",         "092E20", "django",              "white"),
        ("Flask",          "000000", "flask",               "white"),
        ("FastAPI",        "009688", "fastapi",             "white"),
        # Data
        ("Apache%20Spark", "E25A1C", "apachespark",         "white"),
        ("PostgreSQL",     "4169E1", "postgresql",          "white"),
        ("MongoDB",        "47A248", "mongodb",             "white"),
    ]

    lines = []
    for label, color, logo, font_color in badge_list:
        badge = f"![{label}](https://img.shields.io/badge/{label}-{color}?style=for-the-badge&logo={logo}&logoColor={font_color})"
        lines.append(badge)

    # 5 per row
    rows = []
    for i in range(0, len(lines), 5):
        rows.append(" ".join(lines[i:i+5]))
    return "\n\n".join(rows)

# ── Profile Views ─────────────────────────────────────────────────────────────

def profile_views():
    return f"![Profile Views](https://komarev.com/ghpvc/?username={GITHUB_USERNAME}&color=0891b2&style=for-the-badge&label=PROFILE+VIEWS)"

# ── Fetch Top Repos via GitHub API ────────────────────────────────────────────

def fetch_top_repos():
    try:
        url = f"https://api.github.com/users/{GITHUB_USERNAME}/repos?per_page=100&sort=updated"
        req = urllib.request.Request(url, headers={"User-Agent": "readme-generator"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            repos = json.loads(resp.read().decode())
        repos = [r for r in repos if not r.get("fork") and r["name"] != GITHUB_USERNAME]
        repos.sort(key=lambda r: r.get("stargazers_count", 0), reverse=True)
        return repos[:6]
    except Exception:
        return []

def repo_cards(repos):
    if not repos:
        return "_Repositories loading..._"
    cards = []
    for repo in repos:
        name = repo["name"]
        card = (
            f"[![{name}](https://github-readme-stats.vercel.app/api/pin/"
            f"?username={GITHUB_USERNAME}&repo={name}&theme=tokyonight&hide_border=true)]"
            f"(https://github.com/{GITHUB_USERNAME}/{name})"
        )
        cards.append(card)
    rows = []
    for i in range(0, len(cards), 2):
        rows.append(" ".join(cards[i:i+2]))
    return "\n\n".join(rows)

# ── README Builder ────────────────────────────────────────────────────────────

def generate():
    now = datetime.now(timezone.utc).strftime("%d %B %Y, %H:%M UTC")
    repos = fetch_top_repos()

    readme = f"""<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=200&section=header&text=Rajesh%20Kumar%20Jogi&fontSize=50&fontColor=fff&animation=twinkling&fontAlignY=35&desc=Computer%20Vision%20Engineer%20%7C%20AI%20Researcher%20%7C%20MSc%20AI%20Student&descAlignY=55&descSize=18" width="100%"/>

{profile_views()}
[![Portfolio](https://img.shields.io/badge/Portfolio-jogi--rajeshkumar.vercel.app-0891b2?style=for-the-badge&logo=vercel&logoColor=white)](https://jogi-rajeshkumar.vercel.app)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-jogi--rajesh--kumar-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/jogi-rajesh-kumar)
[![Email](https://img.shields.io/badge/Email-rajeshkumarjogi.2098%40gmail.com-EA4335?style=for-the-badge&logo=gmail&logoColor=white)](mailto:rajeshkumarjogi.2098@gmail.com)
[![GitHub](https://img.shields.io/badge/GitHub-jogi--rajeshkumar-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/{GITHUB_USERNAME})

</div>

---

## 🧠 Professional Profile

> MSc Artificial Intelligence student with **3+ years** of professional experience specialising in **Computer Vision**, **Machine Learning**, and **Real-Time Analytics**. Proven track record in leading teams to deploy production-level ML modules that optimise system latency and throughput. Currently researching **privacy-preserving Federated Learning** for EEG-based emotion recognition on edge devices. Expert in building cross-platform AI applications and robust security solutions for **healthcare, finance, and government** sectors.

---

## 💼 Professional Experience

### 🟢 AI Agent Developer — Green Environment Ltd, London *(Oct 2025 – Present)*
- 🤖 Designing intelligent AI-driven systems to enhance operational automation for **ECO4** and **GBIS** initiatives
- 🌱 Applying Computer Vision & ML to solve real-world **sustainability challenges** within the Green Deal sector
- 🔗 Collaborating with data engineering and energy assessment teams to improve system efficiency through R&D

### 🔵 Computer Vision Software Engineer (Team Lead) — Boolean Brain Technologies *(Dec 2023 – Aug 2024)*
- ⚡ Led a team integrating Python-based ML modules into production, reducing **API response latency by 25%**
- 🔧 Refactored legacy inference model code, boosting **system throughput by 1.6×**
- 🌐 Developed customised web applications using Django, decreasing **support tickets by 30%**

### 🟠 Computer Vision Engineer — Timing Technologies India Pvt. Ltd *(May 2023 – Nov 2023)*
- 🏛️ Built **facial recognition** and Bib Detection applications for Government Selections across Indian states
- 🔒 Deployed a secure examination browser on **100+ client devices** using PyInstaller
- 🎯 Fine-tuned **YOLOv5** and **ResNet-50** for edge deployment, achieving **>90% precision**

### 🟡 AI/ML Intern — ThoughtGreen Technologies *(Jan 2023 – Apr 2023)*
- 📚 Researched Bib detection algorithms; trained detection models with **PyTorch** and **TensorFlow**
- 🔬 Executed comprehensive model testing, evaluation, and hyperparameter optimisation

### 🔴 Freelance ML Developer — Independent *(2020 – 2022)*
- 👤 Designed biometric facial attendance and fraud detection systems using advanced ML techniques
- 🛠️ Delivered bespoke web-based tools for clients in **finance, transportation, and administration**

---

## 🎓 Education

**🏫 MSc Artificial Intelligence (with Industrial Placement)**
University of East London, London, UK | *Sept 2024 – May 2026*

| Module | Focus |
|--------|-------|
| Intelligent Systems | AI Planning & Reasoning |
| Big Data Analytics | Distributed Processing at Scale |
| Machine Learning on Big Data | Large-scale ML Pipelines |

> 📌 **Dissertation:** *Federated Learning for EEG-Based Emotion Recognition Across Edge Devices*

---

## 🚀 Key Projects

| Project | Description | Stack |
|---------|-------------|-------|
| 🧠 **eeg-fl-emotion** | Privacy-preserving emotion recognition via Federated Learning | PyTorch, FedAvg, Edge Devices |
| 🛰️ **Satellite Object Recognition** | Memory-efficient deep learning for fine-grained object classification | Keras, CNNs, FAIR1M Dataset |
| 🎭 **Real-Time Face Analysis** | Live browser-based age, emotion & gender detection from video | Flask, PyTorch, face-api.js |
| 👁️ **Real-Time CV Monitoring** | Eye state detection & gesture-based volume control | MediaPipe, OpenCV, Dlib |
| 📈 **Financial Portfolio Optimizer** | Stock market optimisation & automated data pipelines | Pandas, NumPy |
| 🖥️ **DevOps Server Monitor** | Server uptime monitor with real-time Telegram alerts | Python, Telegram API |

---

## 🛠️ Technical Arsenal

{badges()}

---

## 📊 GitHub Analytics

<div align="center">

{github_stats_card()}

{github_streak()}

{top_langs_card()}

{activity_graph()}

{profile_trophy()}

</div>

---

## 📌 Featured Repositories

<div align="center">

{repo_cards(repos)}

</div>

---

## 🏆 Certifications

| 🎖️ Certificate | 🏢 Issuer |
|----------------|----------|
| 🤖 Career Essentials in Generative AI | Microsoft & LinkedIn |
| 👁️ OpenAI API: Vision | LinkedIn Learning |
| 🐳 Docker Foundations Professional Certificate | Docker, Inc. |
| 🧮 ML Algorithms | Great Learning |
| 🍓 Raspberry Pi Emergency Alert Helmet — Edge AI | EC-Council |
| 🔐 SQL Injection Attacks — Cybersecurity | EC-Council |
| 🌐 HTML for Programmers | LinkedIn Learning |
| 📡 Networking Fundamentals | Udemy |
| 💼 AI and Business Strategy | LinkedIn |

---

## 📬 Let's Connect

<div align="center">

[![Portfolio](https://img.shields.io/badge/🌐_Portfolio-Visit_Now-0891b2?style=for-the-badge)](https://jogi-rajeshkumar.vercel.app)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=for-the-badge&logo=linkedin)](https://linkedin.com/in/jogi-rajesh-kumar)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-181717?style=for-the-badge&logo=github)](https://github.com/{GITHUB_USERNAME})
[![Email](https://img.shields.io/badge/Email-Say%20Hello-EA4335?style=for-the-badge&logo=gmail)](mailto:rajeshkumarjogi.2098@gmail.com)

</div>

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=100&section=footer" width="100%"/>

*🔄 README auto-updated on **{now}** via GitHub Actions*

</div>
"""

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme)
    print(f"✅ README.md generated successfully at {now}")


if __name__ == "__main__":
    generate()
