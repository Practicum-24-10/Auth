import json
import os
import sys
import uuid

from flask import Flask, request

sys.path.append(os.path.join(os.getcwd(), ".."))

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from opentelemetry.instrumentation.flask import FlaskInstrumentor

from src.api.v1.auth import users_api_bp
from src.api.v1.oauth import oauth_api
from src.api.v1.roles import roles_bp
from src.api.v1.users_role import users_bp
from src.cli import createsuperuser_bp
from src.core.config import config
from src.db.jwt import init_jwt
from src.db.oauth import init_oauth
from src.db.postgres_db import init_db
from src.db.redis_db import init_redis
from src.error_handlers import handle_exception
from src.jaeger_tracer import configure_tracer
from src.openapi.utils import get_apispec, swagger_ui_blueprint

DEBUG = config.debug


app = Flask(__name__)
app.secret_key = str(uuid.uuid4())
init_db(app)
init_redis(app)
init_jwt(app)
init_oauth(app)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["40 per 2 minute"],
    storage_uri=f"redis://{config.redis_host}:{config.redis_port}/0",
    storage_options={"socket_connect_timeout": 30},
    strategy="fixed-window",
)


if not DEBUG:
    FlaskInstrumentor().instrument_app(app)
    configure_tracer()

    @app.before_request
    def before_request():
        request_id = request.headers.get("X-Request-Id")
        if not request_id:
            raise RuntimeError("request id is required")


@app.route("/swagger")
def create_swagger_spec():
    return json.dumps(get_apispec(app).to_dict())


app.register_error_handler(Exception, handle_exception)
app.register_blueprint(createsuperuser_bp)
app.register_blueprint(swagger_ui_blueprint)
app.register_blueprint(roles_bp, url_prefix="/api/v1/roles/")
app.register_blueprint(users_bp, url_prefix="/api/v1/users/")
app.register_blueprint(users_api_bp)
app.register_blueprint(oauth_api)

if __name__ == "__main__":
    app.run(debug=True)
