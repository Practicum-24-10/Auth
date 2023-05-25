import os

import dotenv
from pydantic import BaseSettings


dotenv.load_dotenv()


class AppSettings(BaseSettings):
    db_name: str = 'db_name'
    db_user: str = 'db_user'
    db_password: str = 'db_password'
    db_host: str = 'db_host'
    db_port: str = '5432'
    redis_host: str = "localhost"
    redis_port: int = 6379
    loglevel: str = 'INFO'

config = AppSettings()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
