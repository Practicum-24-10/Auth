from marshmallow import Schema, fields
from marshmallow.validate import Length


class ChangeSchema(Schema):
    username = fields.String(
        required=False, allow_none=True, validate=Length(min=1, max=100)
    )
    password = fields.String(
        required=False, allow_none=True, validate=Length(min=6, max=100)
    )


class LogoutSchema(Schema):
    logout_all = fields.Boolean(required=True)
    refresh_token = fields.String(required=True)


class LoginSchema(Schema):
    username = fields.String(required=True, validate=Length(min=1, max=100))
    password = fields.String(required=True, validate=Length(min=6, max=100))


class SignupSchema(Schema):
    username = fields.String(
        attribute="username", required=True, validate=Length(min=1, max=100)
    )
    password = fields.String(
        attribute="password", required=True, validate=Length(min=6, max=100)
    )


class HistorySchema(Schema):
    username = fields.String(
        attribute="username", required=True, validate=Length(min=1, max=100)
    )
    password = fields.String(
        attribute="password", required=True, validate=Length(min=6, max=100)
    )
