from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS
from .models import db, User
from .routes import main_bp
from .auth import auth_bp

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    # Load configuration
    app.config.from_object('config.Config')

    # Initialize CORS
    CORS(app)

    # Initialize the database with the app
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Register blueprints (routes)
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

    # Create the database tables if they don't exist
    with app.app_context():
        db.create_all()

    return app

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
