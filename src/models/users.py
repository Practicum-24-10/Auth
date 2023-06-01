from uuid import UUID

from werkzeug.security import check_password_hash, generate_password_hash

from src.db.postgres_db import db
from src.models.mixin import Mixin


class User(Mixin):
    __tablename__ = "users"
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    roles = db.relationship(
        "Role", secondary="users_roles", overlaps="roles,users_relation"
    )
    is_superuser = db.Column(db.BOOLEAN(), default=False)
    is_active = db.Column(db.BOOLEAN(), default=True)

    def __init__(
        self,
        username: str,
        password: str,
        id: UUID | None = None,
        is_superuser: bool = False,
    ):
        self.username = username
        self.set_password(password)
        self.is_superuser = is_superuser
        self.id = id

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"<User {self.username}>"
