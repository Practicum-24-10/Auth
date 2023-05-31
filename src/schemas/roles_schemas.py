from marshmallow import Schema, fields, validate


class RoleSchema(Schema):
    id = fields.UUID()
    name = fields.String(required=True, validate=validate.Length(1, 128))


class UsersRoleSchema(Schema):
    role_name = fields.String(required=True, validate=validate.Length(1, 128))


role_schema = RoleSchema()
users_role_schema = UsersRoleSchema()
