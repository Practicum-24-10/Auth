from uuid import UUID

from flask import Request

from src.db.postgres_db import db
from src.models.history import History


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
    def get_user_history_query(cls, user_id: UUID):
        user_history = History.query.filter_by(user_id=user_id).order_by(
            History.login_time.desc()
        )
        return user_history

    @classmethod
    def get_paginate_history(cls, queryset, page, per_page):
        answer = queryset.paginate(page=page, per_page=per_page, error_out=False)
        return answer


history_service = HistoryService()
