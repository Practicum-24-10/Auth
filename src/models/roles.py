from sqlalchemy.dialects.postgresql import UUID

from src.db.postgres_db import db
from src.models.mixin import Mixin


class UsersRole(db.Model):
    __tablename__ = "users_roles"

    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"),
                        primary_key=True)
    role_id = db.Column(UUID(as_uuid=True), db.ForeignKey("roles.id"),
                        primary_key=True)


class Role(Mixin):
    __tablename__ = "roles"

    name = db.Column(db.String, unique=True, nullable=False)
    users = db.relationship(
        "User", secondary="users_roles", overlaps="roles,users_relation"
    )
    permissions = db.relationship(
        "Permission",
        secondary="roles_permissions",
        overlaps="permissions,roles_relation",
    )

    def __repr__(self):
        return f"<Role {self.name}>"
