from uuid import UUID, uuid4

from flask import Request
from flask_jwt_extended import create_access_token, create_refresh_token
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


def get_device_key(uuid: UUID, request: Request):
    user_agent = request.user_agent
    device_key = f"{uuid} {user_agent}"
    return device_key


def get_device_id(uuid: UUID, request: Request):
    """
    Функция возвращает uuid для контроля доступа по устройству
    :param request:
    :param uuid:
    :return:
    """
    device_key = get_device_key(uuid, request)
    device_id = uuid4()
    redis_client.set(device_key, str(device_id))
    return device_id


def get_claims(uuid: UUID, request: Request) -> dict[str]:
    protection_uuid = get_protection(uuid)
    device_id = get_device_id(uuid, request)
    return {
        "permissions": ["vup", "vip"],
        "is_superuser": False,
        "pr_uuid": protection_uuid,
        "device_id": device_id
    }


def generate_tokens(uuid: UUID, request: Request, old_token=None):
    if old_token is None:
        additional_claims = get_claims(uuid, request)
    else:
        additional_claims = {
            "permissions": old_token.get("permissions"),
            "is_superuser": old_token.get("is_superuser"),
            "pr_uuid": old_token.get("pr_uuid"),
            "device_id": old_token.get("device_id"),
        }
    access_token = create_access_token(
        identity=uuid, additional_claims=additional_claims
    )
    refresh_token = create_refresh_token(
        identity=uuid, additional_claims=additional_claims
    )

    return access_token, refresh_token
