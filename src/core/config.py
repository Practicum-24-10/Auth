import os
from datetime import timedelta

import dotenv
from pydantic import BaseSettings

dotenv.load_dotenv()


class AppSettings(BaseSettings):
    service_name: str = "auth-service"
    db_name: str = "db_name"
    db_user: str = "db_user"
    db_password: str = "db_password"
    db_host: str = "postgres"
    db_port: str = "5432"
    redis_host: str = "redis"
    redis_port: str = "6379"
    loglevel: str = "INFO"
    debug: bool = False
    jaeger_agent_host_name: str = "jaeger"
    jaeger_agent_port: int = 6831


class TokensLife(BaseSettings):
    access: int = 100
    refresh: int = 10000
    delta_refresh: timedelta = timedelta(days=30)
    delta_access: timedelta = timedelta(hours=1)


class YandexClient(BaseSettings):
    yandex_client_id: str = ""
    yandex_client_secret: str = ""


class GoogleClient(BaseSettings):
    google_client_id: str = ""
    google_client_secret: str = ""


class VkClient(BaseSettings):
    vk_client_id: str = ""
    vk_client_secret: str = ""


google_cli = GoogleClient()
vk_cli = VkClient()
yandex_cli = YandexClient()
token_life = TokensLife()
config = AppSettings()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEY_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SECRET_KEY = os.path.join(KEY_DIR, os.environ.get("SECRET_KEY", ""))
PUBLIC_KEY = os.path.join(KEY_DIR, os.environ.get("PUBLIC_KEY", ""))
