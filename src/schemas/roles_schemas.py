from marshmallow import Schema, fields, validate


class RoleIdSchema(Schema):
    id = fields.UUID(attribute="id")


class RoleNameSchema(Schema):
    name = fields.String(
        attribute="name", required=True, validate=validate.Length(1, 128)
    )


class RoleSchema(RoleIdSchema, RoleNameSchema):
    pass


class RoleListSchema(Schema):
    roles = fields.Nested(RoleSchema, many=True)


class UsersIdSchema(Schema):
    user_id = fields.UUID(attribute="id")


class UsersRoleSchema(UsersIdSchema, RoleNameSchema):
    pass


class PermissionIdSchema(Schema):
    id = fields.UUID(attribute="id")


class PermissionNameSchema(Schema):
    permission = fields.String(
        attribute="name", required=True, validate=validate.Length(1, 128)
    )


class PermissionSchema(PermissionIdSchema, PermissionNameSchema):
    pass


role_schema = RoleSchema()
role_name_schema = RoleNameSchema()
role_id_schema = RoleIdSchema()
role_list_schema = RoleListSchema()

users_role_schema = UsersRoleSchema()
permission_schema = PermissionSchema()
