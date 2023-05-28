from uuid import UUID

from flask import Request

from src.db.postgres_db import db
from src.models.history import History
from src.schemas.history_shema import HistorySchema


class HistoryService:
    @classmethod
    def add_user_history(cls, user_id: UUID, request: Request) -> None:
        login_history = History(
            user_id=user_id,
            ip=request.remote_addr,
            user_agent=request.user_agent.string,
        )
        db.session.add(login_history)
        db.session.commit()

    @classmethod
    def get_user_history(cls, user_id: UUID) -> list[None, dict]:
        user_history = History.query.filter_by(user_id=user_id).all()
        if user_history is None:
            return []
        else:
            return [HistorySchema().dump(data) for data in user_history]


history_service = HistoryService()
