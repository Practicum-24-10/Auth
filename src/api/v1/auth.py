from http import HTTPStatus

from flask import Blueprint, make_response, request
from flask_jwt_extended import (decode_token, get_jwt, get_jwt_identity,
                                jwt_required)
from jwt import DecodeError
from marshmallow import ValidationError

from src.schemas.users_schemas import (ChangeSchema, LoginSchema, LogoutSchema,
                                       SignupSchema)
from src.services.redis_servis import redis_service
from src.services.utils import generate_tokens
from src.services.users import user_service
from src.services.history import history_service

users_api_bp = Blueprint("api", __name__, url_prefix="/api/v1/auth")


@users_api_bp.route("/signup", methods=["POST"])
def signup():
    try:
        data = SignupSchema().load(request.json)
    except ValidationError as err:
        return make_response(
            {
                "message": "Validation Error",
            },
            HTTPStatus.BAD_REQUEST,
        )
    if user_service.is_data_exists(data):
        return make_response(
            {"message": "This login already exists"}, HTTPStatus.BAD_REQUEST
        )
    user_service.add_user(data)
    return make_response({"message": "New account was registered"},
                         HTTPStatus.OK)


@users_api_bp.route("/login", methods=["POST"])
def login():
    try:
        data = LoginSchema().load(request.json)
    except ValidationError as err:
        return make_response(
            {
                "message": "Validation Error",
            },
            HTTPStatus.BAD_REQUEST,
        )
    user_id = user_service.check_login_data(data["username"], data["password"])
    if user_id is None:
        return make_response(
            {"message": "Login or password wrong"}, HTTPStatus.BAD_REQUEST
        )
    else:
        access_token, refresh_token = generate_tokens(user_id, request)
        history_service.add_user_history(user_id, request)
        return make_response(
            {
                "message": "Login ok",
                "access_token": access_token,
                "refresh_token": refresh_token,
            },
            HTTPStatus.OK,
        )


@users_api_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()
    old_token = get_jwt()["jti"]
    redis_service.kill_refresh(old_token)
    try:
        access_token, refresh_token = generate_tokens(user_id, request)
    except ValueError:
        return make_response({"message": "Access denied."},
                             HTTPStatus.UNAUTHORIZED)

    return make_response(
        {
            "message": "Refresh ok",
            "access_token": access_token,
            "refresh_token": refresh_token,
        },
        HTTPStatus.OK,
    )


@users_api_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    user_id = get_jwt()["sub"]
    try:
        data = LogoutSchema().load(request.json)
    except ValidationError as err:
        return make_response(
            {
                "message": "Validation Error",
            },
            HTTPStatus.BAD_REQUEST,
        )
    redis_service.check_logout_all(user_id, data["logout_all"])
    try:
        jti_refresh = decode_token(data["refresh_token"])["jti"]
    except DecodeError as err:
        return make_response(
            {
                "message": "Bad refresh token",
            },
            HTTPStatus.BAD_REQUEST,
        )
    jti_access = get_jwt()["jti"]
    redis_service.kill_all_tokens(jti_refresh, jti_access)
    return make_response(
        {
            "message": "Logout ok",
        },
        HTTPStatus.OK,
    )


@users_api_bp.route("/change", methods=["POST"])
@jwt_required()
def change():
    try:
        data = ChangeSchema().load(request.json)
    except ValidationError as err:
        return make_response(
            {
                "message": "Validation Error",
            },
            HTTPStatus.BAD_REQUEST,
        )
    user_id = get_jwt()["sub"]
    if not user_service.check_change(data):
        return make_response(
            {
                "message": "No change",
            },
            HTTPStatus.BAD_REQUEST,
        )
    if user_service.is_data_exists(data):
        return make_response(
            {"message": "This login already exists"}, HTTPStatus.BAD_REQUEST
        )
    user_service.change_user_data(user_id, data)
    return make_response(
        {
            "message": "Change ok",
        },
        HTTPStatus.OK,
    )


@users_api_bp.route("/history", methods=["GET"])
@jwt_required()
def history():
    user_id = get_jwt()["sub"]
    user_history = history_service.get_user_history(user_id)
    if not user_history:
        return make_response(
            {
                "message": "Login history is None",
            },
            HTTPStatus.NOT_FOUND,
        )
    return make_response(
        {
            "message": "login history",
            "history": user_history
        },
        HTTPStatus.OK,
    )
