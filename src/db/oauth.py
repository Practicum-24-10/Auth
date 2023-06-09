from authlib.integrations.flask_client import OAuth
from flask import Flask

from src.core.config import google_cli, vk_cli, yandex_cli

oauth = OAuth()


def init_oauth(app: Flask):
    app.config["GOOGLE_CLIENT_ID"] = google_cli.google_client_id
    app.config["GOOGLE_CLIENT_SECRET"] = google_cli.google_client_secret
    app.config["YANDEX_CLIENT_ID"] = yandex_cli.yandex_client_id
    app.config["YANDEX_CLIENT_SECRET"] = yandex_cli.yandex_client_secret
    app.config["VK_CLIENT_ID"] = vk_cli.vk_client_id
    app.config["VK_CLIENT_SECRET"] = vk_cli.vk_client_secret
    oauth.register(
        name="google",
        access_token_url="https://accounts.google.com/o/oauth2/token",
        authorize_url="https://accounts.google.com/o/oauth2/auth",
        api_base_url="https://www.googleapis.com/oauth2/v1/",
        userinfo_endpoint="https://openidconnect.googleapis.com/v1/userinfo",
        client_kwargs={"scope": "email profile"},
    )

    oauth.register(
        name="yandex",
        access_token_url="https://oauth.yandex.ru/token",
        authorize_url="https://oauth.yandex.ru/authorize",
        api_base_url="https://login.yandex.ru/",
        userinfo_endpoint="info",
    )
    oauth.register(
        name="vk",
        access_token_url="https://oauth.vk.ru/access_token",
        authorize_url="https://oauth.vk.ru/authorize",
        api_base_url="https://api.vk.ru/method/",
        client_kwargs={
            "token_placement": "uri",
            "token_endpoint_auth_method": "client_secret_post",
            "scope": "4194304",
        },
        userinfo_endpoint=("users.get?fields=contacts,sex,site,screen_name" 
                           "&v=5.81"),
    )
    oauth.init_app(app)
