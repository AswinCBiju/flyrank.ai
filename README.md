# Flyrank Internship Repository 🚀

Welcome to my repository for the **Flyrank Backend Engineering Internship** (`internship.flyrank.ai`). This repository contains all practical coding assignments, API developments, and database implementations built throughout the program.

---

## 📂 Repository Structure

Each assignment is housed in its own isolated directory containing its code, environment dependencies, documentation, and dedicated screenshot artifacts.

```text
flyrank.ai/
│
├── assignment-1/            # In-Memory CRUD Task API (FastAPI)
├── assignment-2/            # SQLite-backed Task API (FastAPI + SQLite)
│   ├── database/            # SQLite database files
│   ├── images/              # Dedicated assignment images/screenshots
│   ├── main.py              # Application entrypoint
│   ├── requirements.txt     # Python dependencies
│   └── README.md            # Assignment 2 Documentation
│
├── .gitignore               # Environment and cache exclusions
└── README.md                # Main repository documentation
```

---

## 🛠️ Quick Start & General Setup

### 1. Prerequisites
Ensure you have Python 3.10+ and `pip` installed:
```bash
python3 --version
```

### 2. Working on an Assignment
Navigate into any assignment directory to set up its virtual environment and run the code:

```bash
cd assignment-2

# 1. Create virtual environment
python3 -m venv .venv

# 2. Activate virtual environment
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run application server
uvicorn main:app --reload
```

---

## 📋 Assignment Overview

| Assignment | Description | Core Tech Stack | Status |
| :--- | :--- | :--- | :--- |
| **Assignment 1** | In-Memory Task Management API | FastAPI, Python | Completed |
| **Assignment 2** | Persistent Task API with SQLite storage & raw SQL queries | FastAPI, SQLite, Python | Completed |

---

## 🖼️ Media & Screenshots

To keep the repository clean and structured, images and verification screenshots for each assignment are maintained inside their respective `images/` directory (e.g. `assignment-2/images/`).
