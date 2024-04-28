from flask import current_app
from flask_mysqldb import MySQL
from config import Config  # Add this import statement

mysql = MySQL()

def setup_db(app):
    app.config['MYSQL_HOST'] = Config.MYSQL_HOST  # Use Config class
    app.config['MYSQL_USER'] = Config.MYSQL_USER
    app.config['MYSQL_PASSWORD'] = Config.MYSQL_PASSWORD
    app.config['MYSQL_DB'] = Config.MYSQL_DB
    app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
    mysql.init_app(app)