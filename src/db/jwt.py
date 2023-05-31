from datetime import timedelta
from functools import wraps
from http import HTTPStatus

from flask import Flask
from flask_jwt_extended import JWTManager, get_jwt

from src.services.redis_servis import redis_service

jwt = JWTManager()


def check_if_token_is_revoked(request):
    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            jwt_payload = get_jwt()
            if not redis_service.check_all_data(jwt_payload, request):
                return {
                           "message": "Access denied. Token has been revoked."
                       }, HTTPStatus.UNAUTHORIZED
            return func(*args, **kwargs)

        return inner

    return func_wrapper


def init_jwt(app: Flask):
    app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
    app.config["JWT_BLACKLIST_ENABLED"] = True
    app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access", "refresh"]
    jwt.init_app(app)
