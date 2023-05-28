from uuid import UUID

from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError

from src.core.logger import logger
from src.models.roles import UsersRole
from src.services.users_role import UsersRoleService

users_bp = Blueprint("users", __name__)


@users_bp.post("/<uuid:id>/AddRole")
def add_user_role(id):
    user_id = id
    data = request.json
    if not data:
        return {"message": "Data is missing"}, 400
    role_id = data.get("role_id")
    if not role_id:
        return {"message": "Role is missing"}, 400
    try:
        users_role = UsersRole(user_id=user_id, role_id=role_id)
        UsersRoleService.add_users_role(users_role)
    except IntegrityError as e:
        logger.error(str(e))
        return {"message": "This role has already been assigned to the user"}, 500
    except Exception as e:
        logger.error(str(e))
        return {"message": "Failed to assign a role to a user"}, 500
    return {
        "message": "The role was assigned to the user successfully",
    }, 201


@users_bp.delete("/<uuid:id>/DeleteRole")
def delete_user_role(id):
    user_id = id
    data = request.json
    if not data:
        return {"message": "Data is missing"}, 400
    role_id: UUID = data.get("role_id")
    if not role_id:
        return {"message": "Role is missing"}, 400
    try:
        user_role = UsersRoleService.get_users_role(user_id=user_id, role_id=role_id)
        if user_role:
            UsersRoleService.delete_users_role(user_role)
            return {"message": "User's role was revoked successfully"}, 202
    except Exception as e:
        logger.error(str(e))
        return {"message": "Failed to delete a role to a user"}, 500
    return {"message": "No user no role"}, 400
