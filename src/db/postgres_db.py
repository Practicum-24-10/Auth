from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def init_db(app: Flask):
    import src.models
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://auth_user:123qwe@localhost/auth_db'
    db.init_app(app)