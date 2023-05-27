from datetime import datetime

from sqlalchemy.dialects.postgresql import INET

from src.db.postgres_db import db
from src.models.mixin import Mixin


class History(Mixin):
    __tablename__ = "history"

    user_id = db.Column(db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    ip = db.Column(INET())
    device_id = db.Column(db.String)
    user_agent = db.Column(db.String)
    login_time = db.Column(db.TIMESTAMP, nullable=False, default=datetime.now())

    def __repr__(self):
        return f"<History user id {self.user_id}>"
