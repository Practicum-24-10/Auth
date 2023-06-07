import uuid
from datetime import datetime

from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.postgresql import INET, UUID
from user_agents import parse

from src.db.postgres_db import db
from src.models.utills import is_smart_tv


def create_partition(target, connection, **kw) -> None:
    """creating partition by history"""
    connection.execute(
        """CREATE TABLE IF NOT EXISTS "history_smart" PARTITION OF "history" FOR VALUES IN ('smart')"""
    )
    connection.execute(
        """CREATE TABLE IF NOT EXISTS "history_mobile" PARTITION OF "history" FOR VALUES IN ('mobile')"""
    )
    connection.execute(
        """CREATE TABLE IF NOT EXISTS "history_web" PARTITION OF "history" FOR VALUES IN ('web')"""
    )


class History(db.Model):
    __tablename__ = "history"
    __table_args__ = (
        UniqueConstraint("id", "user_device_type"),
        {
            "postgresql_partition_by": "LIST (user_device_type)",
            "listeners": [("after_create", create_partition)],
        },
    )
    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )

    user_id = db.Column(db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    ip = db.Column(INET())
    device_id = db.Column(db.String, default="")
    user_agent = db.Column(db.String)
    login_time = db.Column(db.TIMESTAMP, nullable=False, default=datetime.now())
    user_device_type = db.Column(db.String, primary_key=True)

    def __init__(self, user_id, ip, user_agent):
        self.user_id = user_id
        self.ip = ip
        self.user_agent = user_agent
        self.login_time = datetime.now()
        self.user_device_type = self.get_device_type(user_agent)

    @staticmethod
    def get_device_type(user_agent):
        user_agent_info = parse(user_agent)
        user_agent_string = user_agent.lower()

        if user_agent_info.is_mobile or "tablet" in user_agent_string:
            device_type = "mobile"
        elif is_smart_tv(user_agent_string):
            device_type = "smart"
        else:
            device_type = "web"

        return device_type

    def __repr__(self):
        return f"<History user id {self.user_id}>"
