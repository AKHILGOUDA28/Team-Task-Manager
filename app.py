import os
import logging
from flask import Flask
from flask_login import LoginManager
from config import Config
from models import db, User

logging.basicConfig(level=logging.INFO)

from routes.auth import auth_bp
from routes.project import project_bp
from routes.task import task_bp
from routes.dashboard import dashboard_bp


def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(Config)

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'warning'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.register_blueprint(auth_bp)
    app.register_blueprint(project_bp)
    app.register_blueprint(task_bp)
    app.register_blueprint(dashboard_bp)

    with app.app_context():
        try:
            db.create_all()
            logging.info('Database tables created/verified successfully.')
        except Exception as e:
            logging.error(f'Could not connect to database on startup: {e}')
            logging.error('Check that DATABASE_URL is set correctly in Railway environment variables.')

    return app


app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
