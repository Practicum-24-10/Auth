from datetime import timedelta
from http import HTTPStatus

from flask import Blueprint, make_response, request
from flask_jwt_extended import (decode_token, get_jwt, get_jwt_identity,
                                jwt_required)
from jwt import DecodeError
from marshmallow import ValidationError

from src.db.jwt import jwt
from src.db.postgres_db import db
from src.db.redis_db import redis_client
from src.models import History
from src.models.users import User
from src.schemas.users_schemas import (ChangeSchema, LoginSchema, LogoutSchema,
                                       SignupSchema)
from src.services.utils import generate_tokens

users_api_bp = Blueprint("api", __name__, url_prefix="/api/v1/auth")


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    token_in_redis = redis_client.get(jti)
    if token_in_redis is not None:
        return make_response(
            {"message": "Access denied. Token has been revoked."},
            HTTPStatus.UNAUTHORIZED,
        )
    user_id = jwt_payload["sub"]
    protection_uuid = redis_client.get(user_id)
    if protection_uuid != jwt_payload["pr_uuid"]:
        return make_response(
            {"message": "Access denied. Token has been revoked."},
            HTTPStatus.UNAUTHORIZED,
        )
    return False


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
    search_user = User.query.filter_by(username=data["username"]).first()
    if search_user is not None:
        return make_response(
            {"message": "This login already exists"}, HTTPStatus.BAD_REQUEST
        )
    user = User(username=data["username"], password=data["password"])
    db.session.add(user)
    db.session.commit()

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
    search_user = User.query.filter_by(username=data["username"]).first()
    if search_user is None:
        return make_response(
            {"message": "Login or password wrong"}, HTTPStatus.BAD_REQUEST
        )
    if search_user.check_password(data["password"]):
        access_token, refresh_token = generate_tokens(search_user.id, request)
        history = History(
            user_id=search_user.id,
            ip=request.remote_addr,
            user_agent=request.user_agent.string
        )
        db.session.add(history)
        db.session.commit()
        return make_response(
            {
                "message": "Login ok",
                "access_token": access_token,
                "refresh_token": refresh_token,
            },
            HTTPStatus.OK,
        )
    else:
        return make_response(
            {"message": "Login or password wrong"}, HTTPStatus.BAD_REQUEST
        )


@users_api_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    old_token = get_jwt()["jti"]
    redis_client.set(old_token, "", ex=timedelta(days=30))
    try:
        access_token, refresh_token = generate_tokens(identity)
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
    pipeline = redis_client.pipeline()
    if data["logout_all"]:
        pipeline.delete(user_id)
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
    pipeline.setex(jti_access, timedelta(hours=1), "")
    pipeline.setex(jti_refresh, timedelta(days=30), "")
    pipeline.execute()
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
    # username = request.json.get("username", None)
    # password = request.json.get("password", None)
    if data["username"] is None and data["password"] is None:
        return make_response(
            {
                "message": "No change",
            },
            HTTPStatus.BAD_REQUEST,
        )
    search_user = User.query.filter_by(username=data["username"]).first()
    if search_user is not None:
        return make_response(
            {
                "message": "This login already exists",
            },
            HTTPStatus.BAD_REQUEST,
        )
    change_user = User.query.filter_by(id=user_id).first()
    if data["username"] is not None:
        change_user.username = data["username"]
    if data["password"] is not None:
        change_user.set_password(data["password"])
    db.session.add(change_user)
    db.session.commit()
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
    # username = request.json.get("username", None)
    # password = request.json.get("password", None)
    user_history = History.query.filter_by(user_id=user_id).all()
    if user_history is None:
        return make_response(
            {
                "message": "Login history is None",
            },
            HTTPStatus.NOT_FOUND,
        )
    # change_user = User.query.filter_by(id=user_id).first()
    # db.session.add(change_user)
    # db.session.commit()
    # return make_response(
    #     {
    #         "message": "Change ok",
    #         "history": [user_role_schema.dump(user_role) for user_role in user_role_list]
    #     },
    #     HTTPStatus.OK,
    # )
