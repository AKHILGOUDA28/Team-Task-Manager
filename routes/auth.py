from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Team

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.dashboard'))
    return render_template('home.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        team_name = request.form.get('team_name', '').strip()

        if not email or not password or not team_name:
            flash('All fields are required.', 'error')
            return render_template('auth/login.html')

        # Verify team exists
        team = Team.query.filter(
            db.func.lower(Team.name) == team_name.lower()
        ).first()
        if not team:
            flash('Team not found. Check your team name.', 'error')
            return render_template('auth/login.html')

        # Verify user belongs to that team
        user = User.query.filter_by(email=email, team_id=team.id).first()
        if not user or not check_password_hash(user.password, password):
            flash('Invalid credentials or you do not belong to this team.', 'error')
            return render_template('auth/login.html')

        login_user(user, remember=True)
        return redirect(url_for('dashboard.dashboard'))

    return render_template('auth/login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.dashboard'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        role = request.form.get('role', 'member').strip().lower()
        team_name = request.form.get('team_name', '').strip()

        # Basic validations
        if not all([name, email, password, team_name]):
            flash('All fields are required.', 'error')
            return render_template('auth/register.html')
        if '@' not in email:
            flash('Invalid email format.', 'error')
            return render_template('auth/register.html')
        if len(password) < 6:
            flash('Password must be at least 6 characters.', 'error')
            return render_template('auth/register.html')
        if role not in ('admin', 'member'):
            flash('Invalid role.', 'error')
            return render_template('auth/register.html')
        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'error')
            return render_template('auth/register.html')

        if role == 'admin':
            # Admin creates a new team
            if Team.query.filter(db.func.lower(Team.name) == team_name.lower()).first():
                flash(f'Team "{team_name}" already exists. Choose a different name.', 'error')
                return render_template('auth/register.html')
            team = Team(name=team_name)
            db.session.add(team)
            db.session.flush()  # get team.id
        else:
            # Member joins an existing team
            team = Team.query.filter(
                db.func.lower(Team.name) == team_name.lower()
            ).first()
            if not team:
                flash(f'Team "{team_name}" not found. Ask your admin for the exact team name.', 'error')
                return render_template('auth/register.html')

        hashed_pw = generate_password_hash(password)
        user = User(name=name, email=email, password=hashed_pw, role=role, team_id=team.id)
        db.session.add(user)
        db.session.commit()

        flash('Account created! Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
