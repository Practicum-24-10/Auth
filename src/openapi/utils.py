from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask_swagger_ui import get_swaggerui_blueprint

from src.schemas.oauth import SocialSchema
from src.schemas.responses import (ErrorResponseSchema, PaginationSchema,
                                   SuccessResponseSchema,
                                   SuccessTokenResponseSchema,
                                   UserHistoryResponseSchema)
from src.schemas.roles_schemas import (PermissionIdSchema, PermissionSchema,
                                       RoleIdSchema, RoleListSchema,
                                       RoleNameSchema, RoleSchema,
                                       UsersIdSchema, UsersRoleSchema)
from src.schemas.users_schemas import (ChangeSchema, LoginSchema, LogoutSchema,
                                       RefreshSchema, SignupSchema)


def get_apispec(app):
    spec = APISpec(
        title="AuthService",
        version="1.0.0",
        openapi_version="3.0.3",
        plugins=[FlaskPlugin(), MarshmallowPlugin()],
    )

    spec.components.schema("Signup", schema=SignupSchema)
    spec.components.schema("Login", schema=LoginSchema)
    spec.components.schema("Logout", schema=LogoutSchema)
    spec.components.schema("Change", schema=ChangeSchema)
    spec.components.schema("Success", schema=SuccessResponseSchema)
    spec.components.schema("Pagination", schema=PaginationSchema)
    spec.components.schema("SuccessGetTokens", schema=SuccessTokenResponseSchema)
    spec.components.schema("Refresh", schema=RefreshSchema)
    spec.components.schema("SuccessUserHistory", schema=UserHistoryResponseSchema)
    spec.components.schema("Error", schema=ErrorResponseSchema)
    access_key_scheme = {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "description": "Enter the token with the `Bearer: ` prefix, e.g. 'Bearer abcde12345'",
    }
    refresh_key_scheme = {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "description": "Enter the token with the `Bearer: ` prefix, e.g. 'Bearer abcde12345'",
    }
    spec.components.security_scheme("AccessToken", access_key_scheme)
    spec.components.security_scheme("RefreshToken", refresh_key_scheme)

    spec.components.schema("RoleNameSchema", schema=RoleNameSchema)
    spec.components.schema("UsersRoleSchema", schema=UsersRoleSchema)
    spec.components.schema("RoleIdSchema", schema=RoleIdSchema)
    spec.components.schema("RoleSchema", schema=RoleSchema)
    spec.components.schema("RoleListSchema", schema=RoleListSchema)
    spec.components.schema("PermissionSchema", schema=PermissionSchema)
    spec.components.schema("PermissionIdSchema", schema=PermissionIdSchema)
    spec.components.schema("UsersIdSchema", schema=UsersIdSchema)
    spec.components.schema("SocialSchema", schema=SocialSchema)
    create_tags(spec)

    load_docstrings(spec, app)

    return spec


def create_tags(spec):
    tags = [
        {"name": "Auth", "description": "Сервис Аутификации"},
        {"name": "OAuth", "description": "Сервис Аутификации через соцсети"},
    ]

    for tag in tags:
        spec.tag(tag)


def load_docstrings(spec, app):
    for fn_name in app.view_functions:
        if fn_name == "static":
            continue
        view_fn = app.view_functions[fn_name]
        spec.path(view=view_fn)


SWAGGER_URL = "/docs"
API_URL = "/swagger"

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL, API_URL, config={"app_name": "My App"}
)
