from typing import Any

from flask import Blueprint, request
from marshmallow import Schema, fields, validate
from werkzeug.exceptions import NotFound

from src.core.logger import logger
from src.models.roles import Role
from src.services.roles import RoleService

roles_bp = Blueprint("roles", __name__)


class RoleSchema(Schema):
    id = fields.String(required=True, validate=validate.Length(1, 128))
    name = fields.String(required=True, validate=validate.Length(1, 128))


role_schema = RoleSchema()


@roles_bp.post("/create")
def add_role():
    data = request.json
    if not data:
        return {"message": "Data is missing"}, 400

    name = data.get("name")
    if not name:
        return {"message": "Name is missing"}, 400

    role = Role(name=name)
    try:
        RoleService.add_role(role)
    except Exception as e:
        logger.error(str(e))
        return {"message": "Failed to add role"}, 500

    return {
        "id": role.id,
        "name": role.name,
    }, 201


@roles_bp.patch("/update/<uuid:id>")
def update_role(id) -> tuple[dict[str, Any], int]:
    data = request.json
    if not data:
        return {"message": "Data is missing"}, 400
    name = data.get("name")
    if not name:
        return {"message": "Role name is missing"}, 400
    try:
        role: Role = RoleService.get_role(id)
        RoleService.update_role(role, name)
        return {
            "id": role.id,
            "name": role.name,
        }, 200
    except NotFound as e:
        logger.error(str(e))
        return {"message": "Role not found"}, 404
    except Exception as e:
        logger.error(str(e))
        return {"message": "Failed to update role"}, 500


@roles_bp.delete("/delete/<id>")
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
