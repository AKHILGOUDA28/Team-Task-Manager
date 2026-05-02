from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Project, User, Task

project_bp = Blueprint('project', __name__)


def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_admin:
            flash('Admin access required.', 'error')
            return redirect(url_for('dashboard.dashboard'))
        return f(*args, **kwargs)
    return decorated


@project_bp.route('/projects')
@login_required
def projects():
    tid = current_user.team_id
    all_projects = Project.query.filter_by(team_id=tid).order_by(Project.created_at.desc()).all()
    return render_template('projects/list.html', projects=all_projects)


@project_bp.route('/projects/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_project():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()

        if not name:
            flash('Project name is required.', 'error')
            return render_template('projects/new.html')

        project = Project(
            name=name,
            description=description,
            team_id=current_user.team_id,
            created_by=current_user.id
        )
        db.session.add(project)
        db.session.commit()

        flash(f'Project "{name}" created!', 'success')
        return redirect(url_for('project.project_detail', project_id=project.id))

    return render_template('projects/new.html')


@project_bp.route('/projects/<int:project_id>')
@login_required
def project_detail(project_id):
    # Security: only same-team projects
    project = Project.query.filter_by(id=project_id, team_id=current_user.team_id).first_or_404()

    tasks = Task.query.filter_by(project_id=project_id, team_id=current_user.team_id)\
        .order_by(Task.created_at.desc()).all()
    team_members = User.query.filter_by(team_id=current_user.team_id).all()

    return render_template(
        'projects/detail.html',
        project=project,
        tasks=tasks,
        team_members=team_members,
        now=__import__('datetime').datetime.utcnow()
    )


@project_bp.route('/projects/<int:project_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_project(project_id):
    project = Project.query.filter_by(id=project_id, team_id=current_user.team_id).first_or_404()
    name = project.name
    db.session.delete(project)
    db.session.commit()
    flash(f'Project "{name}" deleted.', 'info')
    return redirect(url_for('project.projects'))
