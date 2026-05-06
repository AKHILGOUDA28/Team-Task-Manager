from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Task, User, Project

task_bp = Blueprint('task', __name__)

VALID_STATUSES = ('pending', 'in-progress', 'done')
VALID_PRIORITIES = ('low', 'medium', 'high')


def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_admin:
            flash('Admin access required.', 'error')
            return redirect(url_for('dashboard.dashboard'))
        return f(*args, **kwargs)
    return decorated


def parse_deadline(s):
    if not s:
        return None
    try:
        return datetime.strptime(s[:10], '%Y-%m-%d')
    except ValueError:
        return None


@task_bp.route('/tasks')
@login_required
def tasks():
    tid = current_user.team_id
    status_filter = request.args.get('status', '')
    priority_filter = request.args.get('priority', '')
    project_id = request.args.get('project_id', type=int)

    if current_user.is_admin:
        query = Task.query.filter_by(team_id=tid)
    else:
        query = Task.query.filter_by(team_id=tid, assigned_to=current_user.id)

    if project_id:
        query = query.filter_by(project_id=project_id)
    if status_filter in VALID_STATUSES:
        query = query.filter_by(status=status_filter)
    if priority_filter in VALID_PRIORITIES:
        query = query.filter_by(priority=priority_filter)

    all_tasks = query.order_by(Task.created_at.desc()).all()
    projects = Project.query.filter_by(team_id=tid).all()

    return render_template(
        'tasks/list.html',
        tasks=all_tasks,
        projects=projects,
        status_filter=status_filter,
        priority_filter=priority_filter,
        project_id=project_id,
        now=datetime.utcnow()
    )


@task_bp.route('/tasks/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_task():
    tid = current_user.team_id
    projects = Project.query.filter_by(team_id=tid).all()
    members = User.query.filter_by(team_id=tid).all()

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        assigned_to_ids = request.form.getlist('assigned_to', type=int)
        project_id = request.form.get('project_id', type=int)
        deadline = parse_deadline(request.form.get('deadline', ''))
        status = request.form.get('status', 'pending')
        priority = request.form.get('priority', 'medium')

        if not title:
            flash('Task title is required.', 'error')
            return render_template('tasks/new.html', projects=projects, members=members)
        if not project_id:
            flash('Please select a project.', 'error')
            return render_template('tasks/new.html', projects=projects, members=members)
        if not Project.query.filter_by(id=project_id, team_id=tid).first():
            flash('Invalid project.', 'error')
            return render_template('tasks/new.html', projects=projects, members=members)
        if status not in VALID_STATUSES or priority not in VALID_PRIORITIES:
            flash('Invalid status or priority.', 'error')
            return render_template('tasks/new.html', projects=projects, members=members)

        if assigned_to_ids:
            for uid in assigned_to_ids:
                task = Task(
                    title=title, description=description,
                    status=status, priority=priority,
                    assigned_to=uid,
                    project_id=project_id,
                    team_id=tid,
                    deadline=deadline
                )
                db.session.add(task)
            flash(f'Separate tasks created for {len(assigned_to_ids)} members!', 'success')
        else:
            task = Task(
                title=title, description=description,
                status=status, priority=priority,
                assigned_to=None,
                project_id=project_id,
                team_id=tid,
                deadline=deadline
            )
            db.session.add(task)
            flash(f'Unassigned task "{title}" created!', 'success')

        db.session.commit()
        return redirect(url_for('task.tasks'))

    return render_template('tasks/new.html', projects=projects, members=members)


@task_bp.route('/tasks/<int:task_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    tid = current_user.team_id
    task = Task.query.filter_by(id=task_id, team_id=tid).first_or_404()

    if not current_user.is_admin and task.assigned_to != current_user.id:
        flash('You can only edit tasks assigned to you.', 'error')
        return redirect(url_for('task.tasks'))

    projects = Project.query.filter_by(team_id=tid).all() if current_user.is_admin else []
    members = User.query.filter_by(team_id=tid).all() if current_user.is_admin else []

    if request.method == 'POST':
        if current_user.is_admin and 'title' in request.form:
            title = request.form.get('title', '').strip()
            if not title:
                flash('Title cannot be empty.', 'error')
                return render_template('tasks/edit.html', task=task, projects=projects, members=members)
            task.title = title
            task.description = request.form.get('description', '').strip()
            task.assigned_to = request.form.get('assigned_to', type=int) or None
            pid = request.form.get('project_id', type=int)
            if pid and Project.query.filter_by(id=pid, team_id=tid).first():
                task.project_id = pid
            task.deadline = parse_deadline(request.form.get('deadline', ''))
            p = request.form.get('priority', 'medium')
            if p in VALID_PRIORITIES:
                task.priority = p

        s = request.form.get('status', task.status)
        if s in VALID_STATUSES:
            task.status = s

        db.session.commit()
        flash('Task updated!', 'success')
        return redirect(url_for('task.tasks'))

    return render_template('tasks/edit.html', task=task, projects=projects, members=members)


@task_bp.route('/tasks/<int:task_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_task(task_id):
    task = Task.query.filter_by(id=task_id, team_id=current_user.team_id).first_or_404()
    title = task.title
    db.session.delete(task)
    db.session.commit()
    flash(f'Task "{title}" deleted.', 'info')
    return redirect(url_for('task.tasks'))
