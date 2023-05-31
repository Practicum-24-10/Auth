from uuid import UUID

from flask import Request

from src.core.config import token_life
from src.db.redis_db import redis_client
from src.services.utils import get_device_key


class RedisService:
    @classmethod
    def is_token_in_blacklist(cls, token: str) -> bool:
        if redis_client.get(token) is not None:
            return True
        else:
            return False

    @classmethod
    def check_protection_id(cls, user_id: UUID, token_pr_id: UUID) -> bool:
        protection_uuid = redis_client.get(user_id)
        if protection_uuid != token_pr_id:
            return False
        else:
            return True

    @classmethod
    def kill_refresh(cls, refresh_token: str) -> None:
        redis_client.set(refresh_token, "", ex=token_life.delta_refresh)

    @classmethod
    def check_logout_all(cls, user_id: UUID, logout_all: bool):
        if logout_all:
            redis_client.delete(user_id)

    @classmethod
    def check_all_data(cls, jwt_payload: dict, request: Request):
        jti = jwt_payload["jti"]
        user_id = jwt_payload["sub"]
        token_pr_id = jwt_payload["pr_uuid"]
        device_id = jwt_payload["device_id"]
        device_key = get_device_key(user_id, request)
        data = redis_client.mget([jti, user_id, device_key])
        if data[0] is not None:
            return False
        if data[1] != token_pr_id:
            return False
        if data[2] != device_id:
            return False
        return True


redis_service = RedisService()
