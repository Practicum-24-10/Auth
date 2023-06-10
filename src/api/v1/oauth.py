import uuid
from http import HTTPStatus

from flask import Blueprint, make_response, request, url_for

from src.db.oauth import oauth
from src.services.history import history_service
from src.services.social import social_service
from src.services.users import user_service
from src.services.utils import generate_tokens

oauth_api = Blueprint("oauth", __name__, url_prefix="/api/v1/oauth")


@oauth_api.route("/<string:social>")
def oauth_func(social: str):
    """
    ---
    get:
      summary: Изменить роль
      parameters:
        - name: social
          in: path
          description: Название сервиса OAuth
          required: true
          schema: SocialSchema
      responses:
        '302':
          description: Redirect
        '400':
           description: Error
           content:
             application/json:
               schema: ErrorResponseSchema
      tags:
        - OAuth
    """
    client = oauth.create_client(social)
    if client is None:
        return make_response(
            {
                "message": "Social name Error",
            },
            HTTPStatus.BAD_REQUEST,
        )
    redirect_uri = url_for("oauth.authorize", social=social, _external=True)
    return client.authorize_redirect(redirect_uri)


@oauth_api.route("/authorize/<string:social>")
def authorize(social: str):
    """
    ---
    get:
      summary: Колбек авторизации
      parameters:
        - name: social
          in: path
          description: Название сервиса OAuth
          required: true
          schema: SocialSchema
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema: SuccessTokenResponseSchema
        '400':
           description: Error
           content:
             application/json:
               schema: ErrorResponseSchema
      tags:
        - OAuth
    """
    client = oauth.create_client(social)
    if client is None:
        return make_response(
            {
                "message": "Social name Error",
            },
            HTTPStatus.BAD_REQUEST,
        )
    token = client.authorize_access_token()
    social_id, email = social_service.get_userinfo(social, client, token)
    search_user = social_service.is_registered(social_id, social)
    if search_user is None:
        new_user = {"username": str(uuid.uuid4()), "password": str(uuid.uuid4())}
        user_id = user_service.add_user(new_user)
        social_service.add_user(social_id, social, user_id, email)
    else:
        user_id = search_user.user_id
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
