from datetime import timedelta
from uuid import UUID, uuid4

from flask import make_response, Request
from flask_jwt_extended import (JWTManager, create_access_token,
                                create_refresh_token, get_jwt,
                                get_jwt_identity, verify_jwt_in_request)
from werkzeug.local import LocalProxy

from src.core.config import token_life
from src.db.redis_db import redis_client
from src.models.users import User


def get_protection(uuid: UUID):
    """
    Функция возвращает uuid для контроля доступа по всему аккаунту
    Если protection_uuid еще существует, устанавливается новый
    :param uuid:
    :return:
    """
    protection_uuid = redis_client.get(str(uuid))
    if protection_uuid is None:
        protection_uuid = uuid4()
        redis_client.set(str(uuid), str(protection_uuid))
    return protection_uuid


def get_claims(uuid: UUID, request: Request) -> dict[str]:
    protection_uuid = get_protection(uuid)
    return {
        "permissions": ["vup", "vip"],
        "is_superuser": False,
        "pr_uuid": protection_uuid,
    }


def generate_tokens(uuid: UUID, request: Request):
    user = User.query.filter_by(id=uuid).first()
    if not user:
        raise ValueError("User not exists", uuid)
    additional_claims = get_claims(uuid, request)
    access_token = create_access_token(
        identity=uuid, additional_claims=additional_claims
    )
    refresh_token = create_refresh_token(
        identity=uuid, additional_claims=additional_claims
    )

    return access_token, refresh_token
