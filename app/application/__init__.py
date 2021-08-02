from flask import Flask
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

mysql = MySQL(cursorclass=DictCursor)

def init_app():
    """Initialize the core application."""
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    mysql.init_app(app)

    with app.app_context():
        
        from .home.routes import home_bp
        app.register_blueprint(home_bp)

        return app