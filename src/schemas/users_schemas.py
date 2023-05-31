from marshmallow import Schema, fields, validates_schema, ValidationError
from marshmallow.validate import Length


class ChangeSchema(Schema):
    username = fields.String(
        required=True, allow_none=True, validate=Length(min=1, max=100)
    )
    new_password = fields.String(
        required=True, allow_none=True, validate=Length(min=6, max=100)
    )
    old_password = fields.String(
        required=True, allow_none=True, validate=Length(min=6, max=100)
    )

    @validates_schema
    def validate_passwords(self, data, **kwargs):
        new_password = data.get("new_password")
        old_password = data.get("old_password")
        if (new_password is None and old_password is not None) or (
                new_password is not None and old_password is None):
            raise ValidationError("errre")


class RefreshSchema(Schema):
    force = fields.Boolean(required=True)


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
