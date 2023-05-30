from typing import Any

from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from werkzeug.exceptions import NotFound

from db.jwt import check_if_token_is_revoked
from src.core.logger import logger
from src.models.roles import Role
from src.schemas.roles_schemas import role_schema
from src.services.roles import RoleService

roles_bp = Blueprint("roles", __name__)


@roles_bp.post("/create")
@jwt_required()
@check_if_token_is_revoked()
def add_role():
    try:
        data = role_schema.load(request.json)
        name = data.get("name")
        role = Role(name=name)
        RoleService.add_role(role)
    except ValidationError as error:
        return {"message": "Validation error", "errors": error.messages}, 400
    except Exception as e:
        logger.error(str(e))
        return {"message": "Failed to add role"}, 500
    return {
        "id": role.id,
        "name": role.name,
    }, 201


@roles_bp.patch("/update/<uuid:id>")
@jwt_required()
@check_if_token_is_revoked()
def update_role(id) -> tuple[dict[str, Any], int]:
    try:
        data = role_schema.load(request.json)
        name = data.get("name")
        role = RoleService.get_role(id)
        RoleService.update_role(role, name)
        return {
            "id": role.id,
            "name": role.name,
        }, 200
    except ValidationError as error:
        return {"message": "Validation error", "errors": error.messages}, 400
    except NotFound as e:
        logger.error(str(e))
        return {"message": "Role not found"}, 404
    except Exception as e:
        logger.error(str(e))
        return {"message": "Failed to update role"}, 500


@roles_bp.delete("/delete/<id>")
@jwt_required()
@check_if_token_is_revoked()
def delete_role(id):
    try:
        role = RoleService.get_role(id)
        RoleService.delete_role(role)
        return {"message": "Role deleted successfully"}, 202
    except NotFound as e:
        logger.error(str(e))
        return {"message": "Not found"}, 404
    except Exception as e:
        logger.error(str(e))
        return {"message": "Failed to delete role"}, 500


@roles_bp.get("/all")
@jwt_required()
@check_if_token_is_revoked()
def get_all():
    try:
        roles = RoleService.get_all()
        return role_schema.dump(roles, many=True), 200
    except NotFound as e:
        logger.error(str(e))
        return {"message": "Not found"}, 404
    except Exception as e:
        logger.error(str(e))
        return {"message": "Failed"}, 500


@roles_bp.get("/get/<id>")
def get_role(id):
    try:
        role = RoleService.get_role(id)
        if role:
            return {"name": role.name}
    except Exception as e:
        logger.error(str(e))
        return {"message": "Failed to get role"}, 500
    return {"message": "Role not found"}, 404
