"""Initialize Flask Application."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    """Construct the core application."""
    app = Flask(__name__, template_folder="templates")
    app.config.from_pyfile('config.py')

    with app.app_context():
        from . import routes
        db.create_all()
        return app