from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
from src.models import *


def init_db(app: Flask):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://auth_user:123qwe@localhost/auth_db'
    db.init_app(app)
