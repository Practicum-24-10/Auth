from sqlalchemy.dialects.postgresql import UUID

from src.db.postgres_db import db
from src.models.mixin import Mixin


class RolesPermissions(db.Model):
    __tablename__ = "roles_permissions"

    permission_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("permissions.id"), primary_key=True
    )
    role_id = db.Column(UUID(as_uuid=True), db.ForeignKey("roles.id"), primary_key=True)


class Permission(Mixin):
    __tablename__ = "permissions"

    permission = db.Column(db.String, unique=True, nullable=False)
    roles = db.relationship(
        "Role", secondary="roles_permissions", overlaps="permissions,roles_relation"
    )

    def __repr__(self):
        return f"<Permission {self.permission}>"
