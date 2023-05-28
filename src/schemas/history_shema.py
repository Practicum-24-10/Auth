from marshmallow import Schema, fields


class HistorySchema(Schema):
    ip = fields.String(required=True)
    device_id = fields.String(required=True)
    user_agent = fields.String(required=True)
    login_time = fields.String(required=True)
