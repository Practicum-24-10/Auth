from src.db.postgres_db import db
from src.models.roles import UsersRole


class UsersRoleService:
    @classmethod
    def add_user_role(cls, users_role: UsersRole):
        db.session.add(users_role)
        db.session.commit()

    @classmethod
    def get_user_role(cls, user_id, role_id):
        return UsersRole.query.filter_by(user_id=user_id, role_id=role_id).first()

    @classmethod
    def get_user_roles(cls, user_id):
        return UsersRole.query.filter_by(user_id=user_id).all()

    @classmethod
    def delete_users_role(cls, users_role: UsersRole):
        db.session.delete(users_role)
        db.session.commit()
