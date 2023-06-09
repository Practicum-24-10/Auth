from marshmallow import Schema, fields, validate


class SocialSchema(Schema):
    social = fields.String(
        validate=validate.OneOf(["vk", "google", "yandex"]), required=True
    )
