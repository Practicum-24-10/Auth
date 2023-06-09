from src.jaeger_tracer import jaeger_trace
from src.db.postgres_db import db
from src.models.roles import Role


class RoleService:
    @classmethod
    @jaeger_trace
    def add_role(cls, role: Role):
        db.session.add(role)
        db.session.commit()

    @classmethod
    @jaeger_trace
    def get_role(cls, id):
        return db.session.query(Role).get_or_404(id)

    @classmethod
    @jaeger_trace
    def update_role(cls, role: Role, name: str):
        role.name = name
        db.session.commit()

    @classmethod
    @jaeger_trace
    def delete_role(cls, role):
        db.session.delete(role)
        db.session.commit()

    @classmethod
    @jaeger_trace
    def get_all(cls):
        return db.session.query(Role).all()
