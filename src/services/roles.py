from src.models.roles import Role
from src.db.postgres_db import db


class RoleService:
    @classmethod
    def add_role(cls, role: Role):
        db.session.add(role)
        db.session.commit()

    @classmethod
    def delete_role(cls, name: str):
        role = Role.query.filter_by(name=name).first()
        if role:
            db.session.delete(role)
            db.session.commit()
            return f"The {name} role has been successfully deleted"
        else:
            return f"Role {name} does not exist"

    @classmethod
    def get_role(cls, name):
        return Role.query.filter_by(name=name).first()
