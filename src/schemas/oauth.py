from enum import Enum

from marshmallow import Schema, fields, validate


class SocialType(Enum):
    vk = "vk"
    google = "google"
    yandex = "yandex"


class SocialSchema(Schema):
    social = fields.String(
        validate=validate.OneOf([soc.value for soc in SocialType]), required=True
    )
