from typing import Any

from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound

from db.jwt import check_if_token_is_revoked
from services.perm_service import RolePermissionService
from src.services.permissions import auth_required
from src.core.logger import logger
from src.models.permissions import RolesPermissions
from src.models.roles import Role
from src.schemas.roles_schemas import role_schema, permission_schema
from src.services.roles import RoleService

roles_bp = Blueprint("roles", __name__)


@roles_bp.post("/create")
@jwt_required()
@check_if_token_is_revoked()
@auth_required(["RoleControle"])
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


@roles_bp.post("/<uuid:id>/AddPermissions")
@jwt_required()
@check_if_token_is_revoked()
def add_role_permissions(id):
    try:
        role_id = id
        data = permission_schema.load(request.json)
        permission_id = data.get("permission_id")
        role_permission = RolesPermissions(role_id=role_id, permission_id=permission_id)
        RolePermissionService.add_role_permission(role_permission)
    except ValidationError as error:
        return {"message": "Validation error", "errors": error.messages}, 400
    except IntegrityError as e:
        logger.error(str(e))
        return {"message": "This perm has already been assigned to the role"}, 500
    except Exception as e:
        logger.error(str(e))
        return {"message": "Failed to assign a perm to a role"}, 500
    return {
        "message": "The perm was assigned to the role successfully",
    }, 201


@roles_bp.delete("/<uuid:id>/DeletePermissions")
@jwt_required()
@check_if_token_is_revoked()
def delete_role_permission(id):
    try:
        role_id = id
        data = permission_schema.load(request.json)
        permission_id = data.get("permission_id")
        role_permission = RolePermissionService.get_role_permission(
            role_id=role_id, permission_id=permission_id
        )
        if role_permission:
            RolePermissionService.delete_role_permission(role_permission)
            return {"message": "Permission's role was revoked successfully"}, 202
    except ValidationError as error:
        return {"message": "Validation error", "errors": error.messages}, 400
    except Exception as e:
        logger.error(str(e))
        return {"message": "Failed to delete a perm to a role"}, 500
    return {"message": "No role no perm"}, 400
