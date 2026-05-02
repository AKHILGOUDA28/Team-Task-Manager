from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class Team(db.Model):
    __tablename__ = 'teams'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    members = db.relationship('User', backref='team', lazy=True)
    projects = db.relationship('Project', backref='team', lazy=True, cascade='all, delete-orphan')


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='member')  # 'admin' or 'member'
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)

    # Relationships
    created_projects = db.relationship('Project', backref='creator', lazy=True, foreign_keys='Project.created_by')
    assigned_tasks = db.relationship('Task', backref='assignee', lazy=True, foreign_keys='Task.assigned_to')

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def initials(self):
        parts = self.name.split()
        return (parts[0][0] + parts[-1][0]).upper() if len(parts) > 1 else parts[0][:2].upper()


class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    tasks = db.relationship('Task', backref='project', lazy=True, cascade='all, delete-orphan')

    @property
    def task_count(self):
        return len(self.tasks)

    @property
    def completed_count(self):
        return sum(1 for t in self.tasks if t.status == 'done')

    @property
    def progress_pct(self):
        if not self.tasks:
            return 0
        return int((self.completed_count / len(self.tasks)) * 100)


class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='pending')  # pending / in-progress / done
    priority = db.Column(db.String(10), default='medium')  # low / medium / high
    assigned_to = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    deadline = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def is_overdue(self):
        return (
            self.deadline is not None
            and self.deadline < datetime.utcnow()
            and self.status != 'done'
        )

    @property
    def deadline_str(self):
        return self.deadline.strftime('%Y-%m-%d') if self.deadline else ''
