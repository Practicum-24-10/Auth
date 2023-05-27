from flask import Flask
from flask_redis import FlaskRedis

redis_client = FlaskRedis(decode_responses=True)


def init_redis(app: Flask):
    app.config["REDIS_URL"] = "redis://localhost:6379/0"
    app.config["REDIS_DECODE_RESPONSES"] = True
    redis_client.init_app(app)
