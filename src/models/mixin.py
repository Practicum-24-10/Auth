import uuid
from sqlalchemy.dialects.postgresql import UUID
from src.db.postgres_db import db


class Mixin(db.Model):
    __abstract__ = True
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,
                   unique=True, nullable=False)