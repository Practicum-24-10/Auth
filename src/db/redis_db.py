from flask import Flask
from flask_redis import FlaskRedis
from src.core.config import config

redis_client = FlaskRedis(decode_responses=True)


def init_redis(app: Flask):
    app.config["REDIS_URL"] = f"redis://{config.redis_host}:{config.redis_port}/0"
    app.config["REDIS_DECODE_RESPONSES"] = True
    redis_client.init_app(app)
