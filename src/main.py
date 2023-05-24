from flask import Flask
from src.api.v1.roles import roles_bp
from src.db.postgres_db import init_db, db


app = Flask(__name__)

init_db(app)

with app.app_context():
    db.create_all()

app.register_blueprint(roles_bp, url_prefix='/auth/api/v1/')


if __name__ == '__main__':
    app.run(debug=True)
