"""Initialize Flask Application."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
#from flask_redis import FlaskRedis

db = SQLAlchemy()
login_manager = LoginManager()
#r = FlaskRedis()

def create_app():
    """Construct the core app object."""
    app = Flask(__name__, instance_relative_config=False)

    # Application Configuration
    app.config.from_object('config.Config')

    # Initialize Plugins
    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        from app.application.home import routes
        from . import auth
        from .assets import compile_assets

        # Register Blueprints
        app.register_blueprint(routes.main_bp)
        app.register_blueprint(auth.auth_bp)

        # Create Database Models
        db.create_all()

        # Compile static assets
        if app.config['FLASK_ENV'] == 'development':
            compile_assets(app)

        return app
def init_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    db.init_app(app)
    #r.init_app(app)
    with app.app_context():
        from app.application.home import routes
     #   app.register_blueprint(auth.auth_bp)
     #   app.register_blueprint(admin.admin_bp)
        db.create_all()
        return app