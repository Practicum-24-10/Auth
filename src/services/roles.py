from src.db.postgres_db import db
from src.models.roles import Role


class RoleService:
    @classmethod
    def add_role(cls, role: Role):
        db.session.add(role)
        db.session.commit()

    @classmethod
    def get_role(cls, id):
        return db.session.query(Role).get_or_404(id)

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
        return db.session.query(Role).all()
