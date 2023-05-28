from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from src.core.config import config

db = SQLAlchemy()
from src.models import * # noqa


def init_db(app: Flask):
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = f"postgresql://{config.db_user}:{config.db_password}@{config.db_host}/{config.db_name}"
    db.init_app(app)
