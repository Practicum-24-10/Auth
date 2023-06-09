from src.db.postgres_db import db
from src.models.permissions import Permission, RolesPermissions
from src.models.roles import Role


class RolePermissionService:
    @classmethod
    def add_role_permission(cls, role_permission: RolesPermissions):
        db.session.add(role_permission)
        db.session.commit()

    @classmethod
    def get_role_permission(cls, role_id, permission_id):
        return (
            db.session.query(RolesPermissions)
            .filter_by(role_id=role_id, permission_id=permission_id)
            .first()
        )

    @classmethod
    def get_roles_permissions(cls, list_role):
        return (
            db.session.query(Permission)
            .join(RolesPermissions)
            .join(Role)
            .filter(Role.id.in_(list_role))
            .all()
        )

    @classmethod
    def delete_role_permission(cls, role_permission):
        db.session.delete(role_permission)
        db.session.commit()
