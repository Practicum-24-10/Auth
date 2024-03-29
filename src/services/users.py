import uuid
from uuid import UUID

from src.db.postgres_db import db
from src.models.users import User


class UserService:
    @classmethod
    def add_user(cls, data: dict) -> UUID:
        new_id = uuid.uuid4()
        user = User(username=data["username"], password=data["password"], id=new_id)
        db.session.add(user)
        db.session.commit()
        return new_id

    @classmethod
    def is_data_exists(cls, data: dict) -> bool:
        search_user = User.query.filter_by(username=data["username"]).first()
        if search_user is not None:
            return True
        return False

    @classmethod
    def check_data(cls, user_id: str, data: dict) -> str | None:
        check_username = User.query.filter_by(username=data["username"]).first()
        if check_username is not None:
            return "This login already exists"
        search_user = User.query.filter_by(id=user_id).first()
        if search_user is None:
            return "User has been deleted"
        elif data["old_password"] is not None and not search_user.check_password(
            data["old_password"]
        ):
            return "Wrong password"
        return None

    @classmethod
    def check_login_data(cls, username: str, password) -> None | UUID:
        search_user = User.query.filter_by(username=username).first()
        if search_user is None:
            return None
        elif search_user.check_password(password):
            return search_user.id
        else:
            return None

    @classmethod
    def change_user_data(cls, user_id: UUID, data: dict) -> None:
        change_user = User.query.filter_by(id=user_id).first()
        if data["username"] is not None:
            change_user.username = data["username"]
        if data["new_password"] is not None:
            change_user.set_password(data["new_password"])

        db.session.add(change_user)
        db.session.commit()

    @classmethod
    def check_change(cls, data: dict):
        if data["username"] is None and data["new_password"] is None:
            return False
        return True


user_service = UserService()
