from uuid import UUID

from src.db.redis_db import redis_client
from src.core.config import token_life


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
    def kill_all_tokens(cls, refresh_token: str, access_token: str):
        pipeline = redis_client.pipeline()
        pipeline.setex(access_token, token_life.delta_access, "")
        pipeline.setex(refresh_token, token_life.delta_refresh, "")
        pipeline.execute()


redis_service = RedisService()
