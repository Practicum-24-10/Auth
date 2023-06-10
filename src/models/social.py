from sqlalchemy.dialects.postgresql import UUID

from src.db.postgres_db import db
from src.models.mixin import Mixin


class SocialAccounts(Mixin):
    __tablename__ = "social_accounts"

    social_id = db.Column(db.String(200), unique=True, nullable=False)
    social_name = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    user_id = db.Column(db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    users = db.relationship("User", back_populates="social_accounts")

    def __init__(
        self,
        social_id: str,
        social_name: str,
        user_id: str,
        email: str | None = None,
    ):
        self.social_id = social_id
        self.social_name = social_name
        self.user_id = user_id
        self.email = email
