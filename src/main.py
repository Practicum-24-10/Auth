import json

from flask import Flask

from src.api.v1.auth import users_api_bp
from src.api.v1.roles import roles_bp
from src.api.v1.users_role import users_bp
from src.cli import createsuperuser_bp
from src.db.jwt import init_jwt
from src.db.postgres_db import db, init_db
from src.db.redis_db import init_redis
from src.openapi.utils import get_apispec, swagger_ui_blueprint

app = Flask(__name__)
init_db(app)
init_redis(app)
init_jwt(app)


@app.route("/swagger")
def create_swagger_spec():
    return json.dumps(get_apispec(app).to_dict())


with app.app_context():
    db.create_all()
app.register_blueprint(createsuperuser_bp)
app.register_blueprint(swagger_ui_blueprint)
app.register_blueprint(roles_bp, url_prefix="/api/v1/roles/")
app.register_blueprint(users_bp, url_prefix="/api/v1/users/")
app.register_blueprint(users_api_bp)


if __name__ == "__main__":
    app.run(debug=True)
