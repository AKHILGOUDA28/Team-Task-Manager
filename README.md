# 🚀 Ethara AI — Workspace & Team Task Manager

Welcome to **Ethara AI Workspace**, a complete, team-scoped workspace and task orchestration platform designed for modern, data-driven organizations. This platform allows administrators and team members to securely isolate team data, organize critical project milestones, assign tasks, and visualize progress at a glance.

---

## ✨ Features and Capabilities

- **Strict Multi-Tenant Separation**: Every team has its own completely isolated environment where projects, tasks, and dashboards are visible only to authorized team members.
- **Role-Based Access Control (RBAC)**: Fine-grained access privileges separate **Admin** and **Member** permissions to keep work secure.
- **Intelligent Dashboards**: Get live workspace stats including Total, Completed, Pending, In-Progress, and Overdue milestones.
- **Batch Multi-Assignment**: Admins can easily assign tasks to multiple members simultaneously, automatically generating individual task instances.
- **Direct Demo Login**: Quick-access sign-in tools built directly into the authentication portal for accelerated demoing and onboarding.

---

## 🛠️ Technology Stack

*   **Platform Language**: Python 3
*   **Web Framework**: Flask with Flask-Login and Flask-SQLAlchemy ORM
*   **Database**: SQLite for development, natively upgrading to PostgreSQL for production
*   **Aesthetics & CSS**: SaaS light-grey/white custom theme, glassmorphism, responsive micro-animations
*   **Deployment Engine**: High-performance Gunicorn (Procfile-ready for cloud deployments like Railway)

---

## 🗄️ Database Architecture

We maintain absolute structural integrity across the system using the following relational models:

| Entity | Primary Attributes |
|---|---|
| **`Team`** | id, name |
| **`User`** | id, name, email, password, role, team_id |
| **`Project`** | id, name, description, team_id, created_by |
| **`Task`** | id, title, description, status, priority, deadline, assigned_to, project_id, team_id |

---

## ⚙️ How to Set Up the Project Locally

Getting started on your machine takes just a few steps. Follow along below:

```bash
# 1. Clone your GitHub repository
git clone https://github.com/AKHILGOUDA28/Team-Task-Manager.git
cd Team-Task-Manager

# 2. Set up a Python Virtual Environment
python -m venv venv
# On Windows use: venv\Scripts\activate
# On Mac/Linux use: source venv/bin/activate

# 3. Install required packages
pip install -r requirements.txt

# 4. Spin up the local server
python app.py
```

Now, navigate to your favorite browser and open `http://127.0.0.1:5000`!

---

## 🌐 Deploying directly to Railway

Ready to go live in minutes? Follow these steps:

1. Click on **New Project** in your Railway.app dashboard.
2. Connect your GitHub account and select your **`Team-Task-Manager`** repo.
3. Click **+ New** inside the project to provision a **PostgreSQL Database**.
4. Railway will auto-detect both the `requirements.txt` and the `Procfile` and immediately build and launch your application!

---

## 🧑‍💻 Built with Passion

Crafted specifically for intelligent team workflows and high-performance team operations. We hope you enjoy using **Ethara AI Workspace**!
