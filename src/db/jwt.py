from datetime import timedelta
from http import HTTPStatus

from flask import Flask, make_response
from flask_jwt_extended import JWTManager

from src.services.redis_servis import redis_service

jwt = JWTManager()


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    user_id = jwt_payload["sub"]
    token_pr_id = jwt_payload["pr_uuid"]
    if redis_service.is_token_in_blacklist(jti):
        return make_response(
            {"message": "Access denied. Token has been revoked."},
            HTTPStatus.UNAUTHORIZED,
        )
    if not redis_service.check_protection_id(user_id, token_pr_id):
        return make_response(
            {"message": "Access denied. Token has been revoked."},
            HTTPStatus.UNAUTHORIZED,
        )
    return False


def init_jwt(app: Flask):
    app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
    app.config["JWT_BLACKLIST_ENABLED"] = True
    app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access", "refresh"]
    jwt.init_app(app)
