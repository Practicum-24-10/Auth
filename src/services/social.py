from authlib.integrations.flask_client import FlaskOAuth2App
from authlib.oauth2.rfc6749 import OAuth2Token

from src.db.postgres_db import db
from src.models.social import SocialAccounts


class SocialService:
    @classmethod
    def add_user(
            cls, social_id: str, social_name: str, user_id: str, email: str
    ) -> None:
        social_acc = SocialAccounts(
            social_id=social_id, social_name=social_name, user_id=user_id,
            email=email
        )
        db.session.add(social_acc)
        db.session.commit()

    @classmethod
    def is_registered(cls, social_id: str,
                      social: str) -> SocialAccounts | None:
        search_user = SocialAccounts.query.filter_by(
            social_id=social_id, social_name=social
        ).first()
        if search_user is not None:
            return search_user
        return None

    def get_userinfo(self, social: str, client: FlaskOAuth2App,
                     token: OAuth2Token):
        if social == "google":
            return self._get_google_data(client)
        elif social == "vk":
            return self._get_vk_data(token)
        elif social == "yandex":
            return self._get_yandex_data(client)
        userinfo = token.get("userinfo")
        if userinfo is None:
            userinfo = client.userinfo()
        social_id = userinfo["sub"]
        try:
            email = userinfo["email"]
        except KeyError:
            email = None
        return social_id, email

    @classmethod
    def _get_google_data(cls, client: FlaskOAuth2App):
        userinfo = client.userinfo()
        social_id = userinfo["sub"]
        try:
            email = userinfo["email"]
        except KeyError:
            email = None
        return social_id, email

    @classmethod
    def _get_vk_data(cls, token: OAuth2Token):
        social_id = str(token["user_id"])
        try:
            email = token["email"]
        except KeyError:
            email = None
        return social_id, email

    @classmethod
    def _get_yandex_data(cls, client: FlaskOAuth2App):
        userinfo = client.userinfo()
        social_id = userinfo["client_id"]
        try:
            email = userinfo["default_email"]
        except KeyError:
            email = None
        return social_id, email


social_service = SocialService()
