# 🎓 CareerNexus: Intelligent Campus Placement & Career Management Ecosystem

[![Python](https://img.shields.io/badge/Python-3.14-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg)](https://fastapi.tiangolo.com)
[![Database](https://img.shields.io/badge/Database-SQLite%20%7C%20SQLAlchemy-003B57.svg)](https://www.sqlalchemy.org/)
[![Testing](https://img.shields.io/badge/Tests-Pytest%20Passing-brightgreen.svg)](https://docs.pytest.org/)
[![UI](https://img.shields.io/badge/Frontend-TailwindCSS%20%7C%20Lucide-38B2AC.svg)](https://tailwindcss.com/)

> **CareerNexus** is a next-generation campus placement platform designed to bridge the gap between **Students/Job Seekers**, **Placement Cells (TPO)**, **Recruiters**, and **College Alumni**. Unlike legacy ERP noticeboards (Superset, Handshake), CareerNexus delivers proactive diagnostic intelligence, project authenticity verification, automated remediation, and direct talent sourcing.

---

## 🌟 The 7 Core Innovations

1. **Target Company Eligibility & Free Resource Curator**  
   Compares student academic and skill profiles against specific company requirements, highlights missing criteria (CGPA deficit, active backlogs, missing tech skills), and curates verified free learning tracks (FreeCodeCamp, MIT OCW, System Design Primer, roadmap.sh).

2. **Actionable State Improvement Engine ("Level-Up Plan")**  
   Transforms identified gaps into a structured 4-week milestone checklist (Fundamentals -> Proof-of-Work Project -> Google XYZ Resume Refactor -> Mock Drills).

3. **GitHub Profile & Real Project Authenticity Validator**  
   Audits candidate GitHub repositories, inspects commit consistency, code modularity, automated test presence, and filters out copy-pasted tutorial clone templates (Netflix/Todo clones) to award a **Proof-of-Work Score (0–100)** and a **"Verified Project Badge"**.

4. **Intelligent Placement Opportunity Alerts**  
   Priority notification feed with high skill-match alerts (e.g., *"92% Match: Microsoft Campus Drive Opened"*), urgent registration countdowns (*"Registration closes in 14 hours"*), and eligibility tier unlocks.

5. **AI Mock Interview Coach & STAR Evaluator**  
   Company-specific technical and behavioral Q&A simulator. Analyzes student answers using the **STAR framework (Situation, Task, Action, Result)**, scores technical depth, and generates model answer frameworks.

6. **Recruiter "Reverse Pitch" & Direct Talent Sourcing**  
   Enables visiting recruiters to bypass traditional job posts by querying the student pool on custom parameters (CGPA, department, and Verified Project Badge = True) to issue direct **"Fast-Track Interview"** invites.

7. **Alumni "Warm Referral" & Mentorship Bridge**  
   Algorithmic matching engine connecting unplaced or shortlisted students with verified campus alumni working at the target hiring company for 15-minute mock prep chats or internal warm referrals.

---

## 🏛️ System Architecture

```text
career-nexus/
├── backend/
│   ├── database.py         # SQLite connection & session management
│   ├── models.py           # SQLAlchemy database tables (Student, Drive, Alumni, etc.)
│   ├── schemas.py          # Pydantic v2 data validation schemas
│   ├── seed_data.py        # Realistic multi-branch seed dataset
│   ├── main.py             # FastAPI entrypoint & router orchestration
│   ├── services/           # Business logic & AI algorithms
│   │   ├── criteria_engine.py    # Gap analysis & free resource mapping
│   │   ├── github_service.py     # Repo audit & clone detection
│   │   ├── interview_service.py  # STAR answer evaluation & question bank
│   │   ├── alert_service.py      # Opportunity & deadline alert engine
│   │   └── alumni_service.py     # Alumni matching & booking
│   └── routers/            # Clean REST API endpoints
│       ├── students.py
│       ├── drives.py
│       ├── diagnostics.py
│       ├── github_validator.py
│       ├── alerts.py
│       ├── mock_interview.py
│       ├── recruiter.py
│       ├── alumni.py
│       ├── analytics.py
│       └── applications.py
├── frontend/               # Responsive Single-Page Application (SPA)
│   ├── index.html          # Multi-persona dashboard (Student, Recruiter, TPO)
│   ├── app.js              # Reactive state management & API client
│   └── styles.css          # Tailwind glassmorphism styling
├── tests/
│   └── test_ecosystem.py   # Automated pytest verification suite
├── .vscode/
│   ├── settings.json       # VS Code Python environment config
│   └── launch.json         # 1-Click F5 Debug & Run config
├── requirements.txt
├── run.sh                  # One-click runner script
└── README.md
```

---

## 🚀 Quickstart Guide

### 1. Prerequisites
- Python 3.10+ (Built with Python 3.14 on macOS)
- Any modern web browser (Chrome, Safari, Firefox, Edge)

### 2. Run with One Command (Terminal)
```bash
# Clone the repository
git clone https://github.com/<your-username>/CareerNexus.git
cd CareerNexus

# Run the launch script (auto-creates venv & runs server)
./run.sh
```

### 3. Run in VS Code (1-Click)
1. Open the `CareerNexus` folder in **Visual Studio Code**.
2. Press **F5** (or go to **Run & Debug** -> click **Run CareerNexus (FastAPI)**).
3. The server starts automatically on port 8000!

---

## 🌐 Opening the Application

Once running, access the web platform at:
* 🖥️ **Full Dashboard UI**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
* 📖 **Interactive Swagger API Docs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🧪 Running Automated Tests

CareerNexus includes a full automated test suite verifying business logic, database queries, and API endpoints:

```bash
# Activate virtual environment
source .venv/bin/activate

# Execute pytest suite
pytest -v
```

All 7 test cases will execute:
- ✅ Health check & schema validation
- ✅ Student & drive catalog queries
- ✅ Gap analysis & curated free resource resolution
- ✅ GitHub authenticity audit & clone detection
- ✅ STAR mock interview evaluator
- ✅ Recruiter reverse pitch candidate filtering

---

## 📤 How to Push to Your GitHub Account

Run these commands in your project directory:

```bash
# 1. Initialize git (already done) and verify status
git status

# 2. Add your GitHub remote repository (replace with your GitHub URL)
git remote add origin https://github.com/<your-username>/CareerNexus.git

# 3. Ensure branch is named main
git branch -M main

# 4. Push code to GitHub
git push -u origin main
```

---

## 📄 License
This project is open-source and available under the [MIT License](LICENSE).
