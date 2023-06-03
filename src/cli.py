import click
from flask import Blueprint

from src.db.postgres_db import db
from src.models.users import User

createsuperuser_bp = Blueprint("create", __name__)


@createsuperuser_bp.cli.command("superuser")
@click.option("--username", prompt=True, help="Имя пользователя")
@click.option(
    "--password", prompt=True, hide_input=True, confirmation_prompt=True, help="Пароль"
)
def create_superuser(username, password):
    user = db.session.query(User).filter_by(username=username).first()
    if user:
        click.echo(
            click.style("Пользователь с таким username уже существует", fg="yellow")
        )
        return

    user = User(username=username, password=password, is_superuser=True)
    db.session.add(user)
    db.session.commit()
    click.echo(click.style("Суперпользователь успешно создан.", fg="green"))
