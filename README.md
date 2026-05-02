# 🚀 Team Task Manager

A full-stack **team-scoped task management** web application built with **Flask + Jinja2** (server-side rendering). No React, no build step — just Python, HTML and CSS.

---

## ✨ Features

- **Multi-team isolation** — every project, task and dashboard is scoped to a team
- **Role-based access control** — Admin vs Member with strict enforcement
- **Team onboarding** — Admin creates a team; Members join by team name
- **Dashboard** — live stats: Total, Completed, Pending, In-Progress, Overdue
- **Task lifecycle** — Pending → In Progress → Done (color-coded)
- **Overdue detection** — `deadline < now AND status != done`
- **Inline status update** — Members can update their own task status directly from any card

---

## 🗄️ Data Model

| Table | Key Fields |
|---|---|
| `teams` | id, name |
| `users` | id, name, email, password (hashed), role, team_id |
| `projects` | id, name, description, team_id, created_by |
| `tasks` | id, title, description, status, priority, deadline, assigned_to, project_id, team_id |

---

## 🔐 Auth Flow

### Signup
- **Admin** → creates a new team with the given team name
- **Member** → joins an existing team (must enter exact team name)

### Login
- Email + Password + Team Name
- Backend verifies: user exists, password correct, belongs to that team

---

## 🛡️ RBAC Rules

| Action | Admin | Member |
|---|---|---|
| Create project | ✅ | ❌ |
| Create task | ✅ | ❌ |
| Assign tasks | ✅ | ❌ |
| View all team tasks | ✅ | ❌ |
| View own tasks | ✅ | ✅ |
| Update own task status | ✅ | ✅ |
| Delete task/project | ✅ | ❌ |

---

## 🌐 Routes

| Method | URL | Description |
|---|---|---|
| GET | `/` | Redirect to dashboard or login |
| GET/POST | `/login` | Login with team name |
| GET/POST | `/register` | Signup — create or join team |
| GET | `/logout` | Logout |
| GET | `/dashboard` | Team-scoped stats + task cards |
| GET | `/projects` | List team projects |
| GET/POST | `/projects/new` | Create project (admin) |
| GET | `/projects/<id>` | Project detail + tasks |
| POST | `/projects/<id>/delete` | Delete project (admin) |
| GET | `/tasks` | All/assigned tasks + filters |
| GET/POST | `/tasks/new` | Create task (admin) |
| GET/POST | `/tasks/<id>/edit` | Edit task / update status |
| POST | `/tasks/<id>/delete` | Delete task (admin) |

---

## ⚙️ Local Setup

```bash
# 1. Clone the repo
git clone <your-repo-url>
cd "Team Task Manager/backend"

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env   # Edit SECRET_KEY

# 4. Run
python app.py
```

Open `http://localhost:5000`

---

## 🚀 Deploy to Railway

1. Push the `backend/` folder contents to a GitHub repo
2. Create a new Railway project → Deploy from GitHub
3. Set environment variables:

| Variable | Value |
|---|---|
| `SECRET_KEY` | a strong random string |
| `DATABASE_URL` | auto-set by Railway Postgres plugin |

4. Railway auto-detects `Procfile`: `web: gunicorn app:app`

---

## 🎥 Demo Script (2–5 min)

1. Register as **Admin** → create team "DevTeam"
2. Create a **Project** → "Website Redesign"
3. Create a **Task** → assign to member
4. Register as **Member** → join "DevTeam"
5. Member sees only assigned task → updates status to **Done**
6. Admin dashboard shows updated counts

---

## ✅ Success Checklist

- [x] Auth works (signup / login / logout)
- [x] RBAC enforced (admin vs member)
- [x] Team isolation (no cross-team data leaks)
- [x] Full CRUD — Projects & Tasks
- [x] Dashboard stats (total / completed / pending / in-progress / overdue)
- [x] Task lifecycle color-coded (yellow / blue / green / red)
- [x] Inline status update from task card
- [x] Procfile ready for Railway
- [x] PostgreSQL-compatible (via DATABASE_URL)
