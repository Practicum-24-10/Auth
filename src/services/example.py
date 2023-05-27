from typing import List

from src.models.users import User


class UsersService:
    users = []

    @classmethod
    def add_user(cls, user: User):
        cls.users.append(user)

    @classmethod
    def get_all_users(cls) -> List[User]:
        return cls.users
