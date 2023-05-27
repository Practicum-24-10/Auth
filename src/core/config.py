import os

import dotenv
from pydantic import BaseSettings

dotenv.load_dotenv()


class AppSettings(BaseSettings):
    db_name: str = "db_name"
    db_user: str = "db_user"
    db_password: str = "db_password"
    db_host: str = "localhost"
    db_port: str = "5432"
    redis_host: str = "localhost"
    redis_port: str = "6379"
    loglevel: str = "INFO"


class TokensLife(BaseSettings):
    access: int = 100
    refresh: int = 10000


token_life = TokensLife()
config = AppSettings()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
