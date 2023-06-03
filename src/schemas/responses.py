from marshmallow import Schema, fields, validates_schema, ValidationError
from marshmallow.validate import Range

from src.schemas.history_shema import HistorySchema


class PaginationSchema(Schema):
    page = fields.Integer(required=False, description='Страница пагинации',
                          default=1, validate=Range(min=1,
                                                    error="Value must be greater than 0"), example=1)
    size = fields.Integer(required=False, description='Размер пагинации',
                          default=10, validate=Range(min=1,
                                                     error="Value must be greater than 0"), example=10)

    @validates_schema
    def validate_passwords(self, data, **kwargs):
        page = data.get("page")
        size = data.get("size")
        if page < 1 or size < 1:
            raise ValidationError("errre")


class SuccessResponseSchema(Schema):
    message = fields.String(required=True,
                            description='Informational message.')


class UserHistoryResponseSchema(Schema):
    message = fields.String(required=True,
                            description='Informational message.')
    history = fields.Nested(HistorySchema, many=True)
    page = fields.Integer(required=True,
                          description='Страница пагинации')
    size = fields.Integer(required=True,
                          description='Размер пагинации')
    total_pages = fields.Integer(required=True,
                                 description='Всего страниц')
    total_items = fields.Integer(required=True,
                                 description='Всего записей')


class SuccessTokenResponseSchema(Schema):
    message = fields.String(required=True,
                            description='Informational message.')
    access_token = fields.String(required=True,
                                 description='Access_token')
    refresh_token = fields.String(required=True,
                                  description='Refresh_token')


class ErrorResponseSchema(Schema):
    message = fields.String(required=True,
                            description='Informational message.')
