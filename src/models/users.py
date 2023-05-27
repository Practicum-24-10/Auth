from src.models.mixin import Mixin
from src.db.postgres_db import db


class User(Mixin):
    __tablename__ = 'users'
    login = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    roles = db.relationship('Role', secondary='users_roles',
                            overlaps="roles,users_relation")
    is_superuser = db.Column(db.BOOLEAN(), default=False)
    is_active = db.Column(db.BOOLEAN(), default=True)

    def __repr__(self):
        return f'<User {self.login}>'
