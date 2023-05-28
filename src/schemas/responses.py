from marshmallow import Schema, fields

from src.schemas.history_shema import HistorySchema


class SuccessResponseSchema(Schema):
    message = fields.String(required=True,
                            description='Informational message.')


class UserHistoryResponseSchema(Schema):
    message = fields.String(required=True,
                            description='Informational message.')
    history = fields.Nested(HistorySchema, many=True)


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
