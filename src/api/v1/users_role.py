from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from src.core.logger import logger
from src.models.roles import UsersRole
from src.schemas.roles_schemas import role_id_schema
from src.services.permissions import auth_required
from src.services.users_role import UsersRoleService

users_bp = Blueprint("users", __name__)


@users_bp.post("/<uuid:id>/AddRole")
@jwt_required()
@auth_required(["AccessControle"])
def add_user_role(id):
    """
       ---
       post:
         summary: Назначить роль пользователю
         security:
          - AccessToken: []
         requestBody:
           content:
             application/json:
               schema: RoleIdSchema
         parameters:
           - name: id
             in: path
             description: id роли
             required: true
             schema: UsersIdSchema
         responses:
           '200':
             description: Success
             content:
               application/json:
                 schema: SuccessResponseSchema
         tags:
           - Role
    """
    try:
        user_id = id
        data = role_id_schema.load(request.json)
        role_id = data.get("id")
        users_role = UsersRole(user_id=user_id, role_id=role_id)
        UsersRoleService.add_user_role(users_role)
    except ValidationError as error:
        return {"message": "Validation error", "errors": error.messages}, 400
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
@jwt_required()
@auth_required(["AccessControle"])
def delete_user_role(id):
    """
       ---
       delete:
         summary: Отобрать роль у пользователя
         security:
          - AccessToken: []
         requestBody:
           content:
             application/json:
               schema: RoleIdSchema
         parameters:
           - name: id
             in: path
             description: id роли
             required: true
             schema: UsersIdSchema
         responses:
           '200':
             description: Success
             content:
               application/json:
                 schema: SuccessResponseSchema
         tags:
           - Role
    """
    try:
        user_id = id
        data = role_id_schema.load(request.json)
        role_id = data.get("id")
        user_role = UsersRoleService.get_user_role(user_id=user_id, role_id=role_id)
        if user_role:
            UsersRoleService.delete_users_role(user_role)
            return {"message": "User's role was revoked successfully"}, 202
    except ValidationError as error:
        return {"message": "Validation error", "errors": error.messages}, 400
    except Exception as e:
        logger.error(str(e))
        return {"message": "Failed to delete a role to a user"}, 500
    return {"message": "No user no role"}, 400
