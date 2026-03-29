"""
generate_readme.py — jogi-rajeshkumar profile README generator
Builds stats SVG cards locally via GitHub API — zero external dependencies.
Run with: python generate_readme.py [--token YOUR_GITHUB_TOKEN]
The workflow passes GITHUB_TOKEN automatically.
"""

import urllib.request
import urllib.parse
import json
import os
import sys
from datetime import datetime, timezone

GITHUB_USERNAME = "jogi-rajeshkumar"

# ── GitHub API helper ─────────────────────────────────────────────────────────

def gh_api(path, token=None):
    url = f"https://api.github.com{path}"
    headers = {"User-Agent": "readme-generator", "Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read().decode())
    except Exception as e:
        print(f"⚠️  API {path}: {e}")
        return None

# ── SVG card builders ─────────────────────────────────────────────────────────

def build_stats_svg(token=None):
    data = gh_api(f"/users/{GITHUB_USERNAME}", token)
    if not data:
        return None
    repos = gh_api(f"/users/{GITHUB_USERNAME}/repos?per_page=100", token) or []
    total_stars = sum(r.get("stargazers_count", 0) for r in repos)
    total_forks = sum(r.get("forks_count", 0) for r in repos)
    followers   = data.get("followers", 0)
    public_repos= data.get("public_repos", 0)

    svg = f"""<svg width="495" height="195" viewBox="0 0 495 195" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#1a1b27"/>
      <stop offset="100%" style="stop-color:#0d1117"/>
    </linearGradient>
  </defs>
  <rect width="495" height="195" rx="10" fill="url(#bg)" stroke="#30363d" stroke-width="1"/>

  <!-- Title -->
  <text x="25" y="35" font-family="Segoe UI,sans-serif" font-size="15" font-weight="700" fill="#58a6ff">
    {GITHUB_USERNAME}'s GitHub Stats
  </text>

  <!-- Stars -->
  <text x="25"  y="80"  font-family="Segoe UI,sans-serif" font-size="13" fill="#8b949e">⭐ Total Stars</text>
  <text x="230" y="80"  font-family="Segoe UI,sans-serif" font-size="13" font-weight="700" fill="#e6edf3">{total_stars:,}</text>

  <!-- Forks -->
  <text x="25"  y="110" font-family="Segoe UI,sans-serif" font-size="13" fill="#8b949e">🍴 Total Forks</text>
  <text x="230" y="110" font-family="Segoe UI,sans-serif" font-size="13" font-weight="700" fill="#e6edf3">{total_forks:,}</text>

  <!-- Followers -->
  <text x="25"  y="140" font-family="Segoe UI,sans-serif" font-size="13" fill="#8b949e">👥 Followers</text>
  <text x="230" y="140" font-family="Segoe UI,sans-serif" font-size="13" font-weight="700" fill="#e6edf3">{followers:,}</text>

  <!-- Repos -->
  <text x="25"  y="170" font-family="Segoe UI,sans-serif" font-size="13" fill="#8b949e">📦 Public Repos</text>
  <text x="230" y="170" font-family="Segoe UI,sans-serif" font-size="13" font-weight="700" fill="#e6edf3">{public_repos:,}</text>

  <!-- Accent bar -->
  <rect x="25" y="47" width="50" height="3" rx="2" fill="#58a6ff"/>
</svg>"""
    return svg


def build_langs_svg(token=None):
    repos = gh_api(f"/users/{GITHUB_USERNAME}/repos?per_page=100", token) or []
    lang_counts = {}
    for repo in repos:
        if repo.get("fork"):
            continue
        lang = repo.get("language")
        if lang:
            lang_counts[lang] = lang_counts.get(lang, 0) + 1

    if not lang_counts:
        return None

    total = sum(lang_counts.values())
    sorted_langs = sorted(lang_counts.items(), key=lambda x: x[1], reverse=True)[:8]

    LANG_COLORS = {
        "Python": "#3572A5", "JavaScript": "#f1e05a", "TypeScript": "#2b7489",
        "HTML": "#e34c26",   "CSS": "#563d7c",        "Java": "#b07219",
        "C++": "#f34b7d",    "C": "#555555",          "Shell": "#89e051",
        "Jupyter Notebook": "#DA5B0B", "Dockerfile": "#384d54",
        "Vue": "#41b883",    "Go": "#00ADD8",          "Rust": "#dea584",
        "Ruby": "#701516",   "Kotlin": "#F18E33",
    }

    bar_width = 445
    rows = ""
    bar_segments = ""
    x_offset = 0

    for lang, count in sorted_langs:
        pct = count / total
        seg_w = round(pct * bar_width)
        color = LANG_COLORS.get(lang, "#8b949e")
        bar_segments += f'<rect x="{25 + x_offset}" y="60" width="{seg_w}" height="8" rx="4" fill="{color}"/>'
        x_offset += seg_w

    y = 95
    for i, (lang, count) in enumerate(sorted_langs):
        pct_label = f"{count/total*100:.1f}%"
        color = LANG_COLORS.get(lang, "#8b949e")
        col = i % 2
        row = i // 2
        cx = 25 + col * 220
        cy = y + row * 25
        rows += f"""
  <circle cx="{cx+6}" cy="{cy-4}" r="5" fill="{color}"/>
  <text x="{cx+16}" y="{cy}" font-family="Segoe UI,sans-serif" font-size="12" fill="#e6edf3">{lang}</text>
  <text x="{cx+185}" y="{cy}" font-family="Segoe UI,sans-serif" font-size="12" fill="#8b949e" text-anchor="end">{pct_label}</text>"""

    height = 95 + ((len(sorted_langs) + 1) // 2) * 25 + 15
    svg = f"""<svg width="495" height="{height}" viewBox="0 0 495 {height}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#1a1b27"/>
      <stop offset="100%" style="stop-color:#0d1117"/>
    </linearGradient>
    <clipPath id="bar-clip">
      <rect x="25" y="58" width="{bar_width}" height="12" rx="6"/>
    </clipPath>
  </defs>
  <rect width="495" height="{height}" rx="10" fill="url(#bg)" stroke="#30363d" stroke-width="1"/>
  <text x="25" y="35" font-family="Segoe UI,sans-serif" font-size="15" font-weight="700" fill="#58a6ff">Most Used Languages</text>
  <rect x="25" y="47" width="50" height="3" rx="2" fill="#58a6ff"/>
  <!-- Background bar -->
  <rect x="25" y="60" width="{bar_width}" height="8" rx="4" fill="#30363d"/>
  <!-- Language segments clipped -->
  <g clip-path="url(#bar-clip)">{bar_segments}</g>
  {rows}
</svg>"""
    return svg


def build_trophies_svg(token=None):
    data  = gh_api(f"/users/{GITHUB_USERNAME}", token) or {}
    repos = gh_api(f"/users/{GITHUB_USERNAME}/repos?per_page=100", token) or []
    followers    = data.get("followers", 0)
    public_repos = data.get("public_repos", 0)
    total_stars  = sum(r.get("stargazers_count", 0) for r in repos)

    def trophy(x, y, emoji, label, value, color="#58a6ff"):
        return f"""
  <rect x="{x}" y="{y}" width="130" height="80" rx="8" fill="#161b22" stroke="{color}" stroke-width="1.5"/>
  <text x="{x+65}" y="{y+28}" font-family="Segoe UI,sans-serif" font-size="22" text-anchor="middle">{emoji}</text>
  <text x="{x+65}" y="{y+52}" font-family="Segoe UI,sans-serif" font-size="13" font-weight="700" fill="{color}" text-anchor="middle">{value}</text>
  <text x="{x+65}" y="{y+68}" font-family="Segoe UI,sans-serif" font-size="10" fill="#8b949e" text-anchor="middle">{label}</text>"""

    trophies = [
        (25,  60, "⭐", "Stars",     total_stars,  "#f1c40f"),
        (165, 60, "📦", "Repos",     public_repos, "#58a6ff"),
        (305, 60, "👥", "Followers", followers,    "#a371f7"),
        (445 if False else 25, 60, "", "", "", ""),  # skip 4th to keep 3-wide
    ]

    svg = f"""<svg width="610" height="165" viewBox="0 0 610 165" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#1a1b27"/>
      <stop offset="100%" style="stop-color:#0d1117"/>
    </linearGradient>
  </defs>
  <rect width="610" height="165" rx="10" fill="url(#bg)" stroke="#30363d" stroke-width="1"/>
  <text x="25" y="40" font-family="Segoe UI,sans-serif" font-size="15" font-weight="700" fill="#58a6ff">GitHub Trophies</text>
  <rect x="25" y="47" width="50" height="3" rx="2" fill="#58a6ff"/>
  {trophy(25,  60, "⭐", "Stars",     f"{total_stars:,}",  "#f1c40f")}
  {trophy(165, 60, "📦", "Repos",     f"{public_repos:,}", "#58a6ff")}
  {trophy(305, 60, "👥", "Followers", f"{followers:,}",    "#a371f7")}
  {trophy(445, 60, "🏫", "University", "UEL",              "#3fb950")}
</svg>"""
    return svg

# ── Write SVGs to disk ────────────────────────────────────────────────────────

def generate_svgs(token=None):
    os.makedirs("assets/stats", exist_ok=True)
    tasks = [
        ("assets/stats/github-stats.svg", build_stats_svg(token)),
        ("assets/stats/top-langs.svg",    build_langs_svg(token)),
        ("assets/stats/trophies.svg",     build_trophies_svg(token)),
    ]
    for path, svg in tasks:
        if svg:
            with open(path, "w", encoding="utf-8") as f:
                f.write(svg)
            print(f"✅ Generated {path}")
        else:
            print(f"⚠️  Skipped {path} (no data)")

# ── Skill Badges ──────────────────────────────────────────────────────────────

def badges():
    badge_list = [
        ("Python",           "3776AB", "python",            "white"),
        ("JavaScript",       "F7DF1E", "javascript",        "black"),
        ("SQL",              "4479A1", "mysql",             "white"),
        ("HTML5",            "E34F26", "html5",             "white"),
        ("CSS3",             "1572B6", "css3",              "white"),
        ("PyTorch",          "EE4C2C", "pytorch",           "white"),
        ("TensorFlow",       "FF6F00", "tensorflow",        "white"),
        ("Keras",            "D00000", "keras",             "white"),
        ("OpenCV",           "5C3EE8", "opencv",            "white"),
        ("HuggingFace",      "FFD21E", "huggingface",       "black"),
        ("scikit--learn",    "F7931E", "scikitlearn",       "white"),
        ("AWS",              "232F3E", "amazonwebservices", "white"),
        ("Docker",           "2496ED", "docker",            "white"),
        ("GitHub%20Actions", "2088FF", "githubactions",     "white"),
        ("Linux",            "FCC624", "linux",             "black"),
        ("Django",           "092E20", "django",            "white"),
        ("Flask",            "000000", "flask",             "white"),
        ("FastAPI",          "009688", "fastapi",           "white"),
        ("Apache%20Spark",   "E25A1C", "apachespark",       "white"),
        ("PostgreSQL",       "4169E1", "postgresql",        "white"),
        ("MongoDB",          "47A248", "mongodb",           "white"),
    ]
    lines = []
    for label, color, logo, font_color in badge_list:
        lines.append(
            f'<img src="https://img.shields.io/badge/{label}-{color}'
            f'?style=for-the-badge&logo={logo}&logoColor={font_color}" alt="{label}"/>'
        )
    rows = []
    for i in range(0, len(lines), 5):
        rows.append("\n".join(lines[i:i+5]))
    return "\n\n".join(rows)

# ── Repo cards ────────────────────────────────────────────────────────────────

def fetch_top_repos(token=None):
    repos = gh_api(f"/users/{GITHUB_USERNAME}/repos?per_page=100&sort=updated", token) or []
    repos = [r for r in repos if not r.get("fork") and r["name"] != GITHUB_USERNAME]
    repos.sort(key=lambda r: r.get("stargazers_count", 0), reverse=True)
    return repos[:6]

def repo_cards(repos):
    if not repos:
        return '<tr><td align="center"><em>Repositories loading...</em></td></tr>'
    cells = []
    for repo in repos:
        name = repo["name"]
        cell = (
            f'<td align="center" width="33%">\n'
            f'<a href="https://github.com/{GITHUB_USERNAME}/{name}">\n'
            f'<img src="https://gh-card.dev/repos/{GITHUB_USERNAME}/{name}.svg?fullname=" '
            f'width="100%" alt="{name}"/>\n'
            f'</a>\n</td>'
        )
        cells.append(cell)
    rows = []
    for i in range(0, len(cells), 3):
        chunk = cells[i:i+3]
        while len(chunk) < 3:
            chunk.append('<td width="33%"></td>')
        rows.append("<tr>\n" + "\n".join(chunk) + "\n</tr>")
    return "\n".join(rows)

# ── README builder ────────────────────────────────────────────────────────────

def generate(token=None):
    now   = datetime.now(timezone.utc).strftime("%d %B %Y, %H:%M UTC")
    repos = fetch_top_repos(token)

    readme = f"""<div align="center">
<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=200&section=header&text=Rajesh%20Kumar%20Jogi&fontSize=50&fontColor=fff&animation=twinkling&fontAlignY=35&desc=Computer%20Vision%20Engineer%20%7C%20AI%20Researcher%20%7C%20MSc%20AI%20Student&descAlignY=55&descSize=18" width="100%"/>

<img src="https://komarev.com/ghpvc/?username={GITHUB_USERNAME}&color=0891b2&style=for-the-badge&label=PROFILE+VIEWS" alt="Profile Views"/>

<a href="https://jogi-rajeshkumar.vercel.app"><img src="https://img.shields.io/badge/Portfolio-jogi--rajeshkumar.vercel.app-0891b2?style=for-the-badge&logo=vercel&logoColor=white" alt="Portfolio"/></a>
<a href="https://linkedin.com/in/jogi-rajesh-kumar"><img src="https://img.shields.io/badge/LinkedIn-jogi--rajesh--kumar-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"/></a>
<a href="mailto:rajeshkumarjogi.2098@gmail.com"><img src="https://img.shields.io/badge/Email-rajeshkumarjogi.2098%40gmail.com-EA4335?style=for-the-badge&logo=gmail&logoColor=white" alt="Email"/></a>
<a href="https://github.com/{GITHUB_USERNAME}"><img src="https://img.shields.io/badge/GitHub-jogi--rajeshkumar-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub"/></a>
</div>

---

## 🧠 Professional Profile

> MSc Artificial Intelligence student with **3+ years** of professional experience specialising in **Computer Vision**, **Machine Learning**, and **Real-Time Analytics**. Proven track record in leading teams to deploy production-level ML modules that optimise system latency and throughput. Currently researching **privacy-preserving Federated Learning** for EEG-based emotion recognition on edge devices. Expert in building cross-platform AI applications and robust security solutions for **healthcare, finance, and government** sectors.

---

## 💼 Professional Experience

### 🟢 AI Agent Developer — Green Environment Ltd, London *(Oct 2025 – Present)*
- 🤖 Designing intelligent AI-driven systems to enhance automation for **ECO4** and **GBIS** initiatives
- 🌱 Applying Computer Vision & ML to real-world **sustainability challenges** within the Green Deal sector
- 🔗 Collaborating with data engineering and energy assessment teams through R&D

### 🔵 Computer Vision Software Engineer (Team Lead) — Boolean Brain Technologies *(Dec 2023 – Aug 2024)*
- ⚡ Led a team integrating Python ML modules into production, reducing **API latency by 25%**
- 🔧 Refactored legacy inference model code, boosting **system throughput by 1.6×**
- 🌐 Developed customised Django web applications, decreasing **support tickets by 30%**

### 🟠 Computer Vision Engineer — Timing Technologies India Pvt. Ltd *(May 2023 – Nov 2023)*
- 🏛️ Built **facial recognition** and Bib Detection apps for Government Selections across Indian states
- 🔒 Deployed a secure examination browser on **100+ client devices** using PyInstaller
- 🎯 Fine-tuned **YOLOv5** and **ResNet-50** for edge deployment, achieving **>90% precision**

### 🟡 AI/ML Intern — ThoughtGreen Technologies *(Jan 2023 – Apr 2023)*
- 📚 Researched Bib detection algorithms; trained models with **PyTorch** and **TensorFlow**
- 🔬 Executed comprehensive model testing, evaluation, and hyperparameter optimisation

### 🔴 Freelance ML Developer — Independent *(2020 – 2022)*
- 👤 Designed biometric facial attendance and fraud detection systems
- 🛠️ Delivered bespoke tools for clients in **finance, transportation, and administration**

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
| 🛰️ **Satellite Object Recognition** | Memory-efficient deep learning for fine-grained classification | Keras, CNNs, FAIR1M Dataset |
| 🎭 **Real-Time Face Analysis** | Live browser-based age, emotion & gender detection | Flask, PyTorch, face-api.js |
| 👁️ **Real-Time CV Monitoring** | Eye state detection & gesture-based volume control | MediaPipe, OpenCV, Dlib |
| 📈 **Financial Portfolio Optimizer** | Stock market optimisation & automated data pipelines | Pandas, NumPy |
| 🖥️ **DevOps Server Monitor** | Server uptime monitor with Telegram alerts | Python, Telegram API |

---

## 🛠️ Technical Arsenal

<div align="center">

{badges()}

</div>

---

## 📊 GitHub Analytics

<div align="center">
<table>
<tr>
<td align="center" width="50%">
<a href="https://github.com/{GITHUB_USERNAME}">
<img src="assets/stats/github-stats.svg" alt="GitHub Stats" width="100%"/>
</a>
</td>
<td align="center" width="50%">
<a href="https://github.com/{GITHUB_USERNAME}">
<img src="https://streak-stats.demolab.com/?user={GITHUB_USERNAME}&theme=tokyonight&hide_border=true" alt="GitHub Streak" width="100%"/>
</a>
</td>
</tr>
<tr>
<td align="center" width="50%">
<a href="https://github.com/{GITHUB_USERNAME}">
<img src="assets/stats/top-langs.svg" alt="Top Languages" width="100%"/>
</a>
</td>
<td align="center" width="50%">
<a href="https://github.com/{GITHUB_USERNAME}">
<img src="https://github-readme-activity-graph.vercel.app/graph?username={GITHUB_USERNAME}&theme=tokyo-night&hide_border=true&area=true" alt="Activity Graph" width="100%"/>
</a>
</td>
</tr>
</table>
</div>

<div align="center">
<a href="https://github.com/{GITHUB_USERNAME}">
<img src="assets/stats/trophies.svg" alt="GitHub Trophies" width="100%"/>
</a>
</div>

---

## 📌 Featured Repositories

<div align="center">
<table>
{repo_cards(repos)}
</table>
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
<a href="https://jogi-rajeshkumar.vercel.app"><img src="https://img.shields.io/badge/Portfolio-Visit_Now-0891b2?style=for-the-badge&logo=vercel&logoColor=white" alt="Portfolio"/></a>
<a href="https://linkedin.com/in/jogi-rajesh-kumar"><img src="https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"/></a>
<a href="https://github.com/{GITHUB_USERNAME}"><img src="https://img.shields.io/badge/GitHub-Follow-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub"/></a>
<a href="mailto:rajeshkumarjogi.2098@gmail.com"><img src="https://img.shields.io/badge/Email-Say%20Hello-EA4335?style=for-the-badge&logo=gmail&logoColor=white" alt="Email"/></a>
</div>

---

<div align="center">
<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=100&section=footer" width="100%"/>

*🔄 README auto-updated on **{now}** via GitHub Actions*
</div>
"""
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme)
    print(f"✅ README.md generated at {now}")


if __name__ == "__main__":
    token = None
    if "--token" in sys.argv:
        idx = sys.argv.index("--token")
        token = sys.argv[idx + 1] if idx + 1 < len(sys.argv) else None
    # Also check env var (set automatically in GitHub Actions)
    if not token:
        token = os.environ.get("GITHUB_TOKEN")

    generate_svgs(token)
    generate(token)
