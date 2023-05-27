from src.models.roles import Role
from src.db.postgres_db import db


class RoleService:
    @classmethod
    def add_role(cls, role: Role):
        db.session.add(role)
        db.session.commit()

    @classmethod
    def get_role(cls, id):
        return Role.query.get_or_404(id)

    @classmethod
    def update_role(cls, role: Role, name: str):
        role.name = name
        db.session.commit()

    @classmethod
    def delete_role(cls, role):
        db.session.delete(role)
        db.session.commit()

    @classmethod
    def get_all(cls):
        return Role.query.all()
