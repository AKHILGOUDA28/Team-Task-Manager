from datetime import datetime
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models import Task, Project, User

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    now = datetime.utcnow()
    tid = current_user.team_id

    if current_user.is_admin:
        tasks = Task.query.filter_by(team_id=tid).all()
        projects = Project.query.filter_by(team_id=tid).order_by(Project.created_at.desc()).all()
        members = User.query.filter_by(team_id=tid).all()
    else:
        tasks = Task.query.filter_by(team_id=tid, assigned_to=current_user.id).all()
        projects = Project.query.filter_by(team_id=tid).all()
        members = []

    total = len(tasks)
    completed = sum(1 for t in tasks if t.status == 'done')
    in_progress = sum(1 for t in tasks if t.status == 'in-progress')
    pending = sum(1 for t in tasks if t.status == 'pending')
    overdue = sum(
        1 for t in tasks
        if t.deadline and t.deadline < now and t.status != 'done'
    )

    recent_tasks = sorted(tasks, key=lambda t: t.created_at, reverse=True)[:5]
    overdue_tasks = [
        t for t in tasks
        if t.deadline and t.deadline < now and t.status != 'done'
    ][:5]

    stats = {
        'total': total,
        'completed': completed,
        'in_progress': in_progress,
        'pending': pending,
        'overdue': overdue,
        'project_count': len(projects),
        'member_count': len(members),
        'completion_pct': int((completed / total * 100) if total else 0),
    }

    return render_template(
        'dashboard/dashboard.html',
        stats=stats,
        tasks=tasks,
        projects=projects[:4],
        now=now,
    )
