from http import HTTPStatus

from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound

from src.core.logger import logger
from src.models.permissions import RolesPermissions
from src.models.roles import Role
from src.schemas.roles_schemas import permission_schema, role_name_schema, role_schema
from src.services.perm_service import RolePermissionService
from src.services.permissions import auth_required
from src.services.roles import RoleService

roles_bp = Blueprint("roles", __name__)


@roles_bp.post("/create")
@jwt_required()
@auth_required(["AccessControle"])
def add_role():
    """
    ---
    post:
      summary: Добавить роль
      security:
       - AccessToken: []
      requestBody:
        content:
          application/json:
            schema: RoleNameSchema
      responses:
        '201':
          description: Created
          content:
            application/json:
              schema: SuccessResponseSchema
      tags:
        - Role
    """
    try:
        data = role_name_schema.load(request.json)
        name = data.get("name")
        role = Role(name=name)
        RoleService.add_role(role)
    except ValidationError as error:
        return {
            "message": "Validation error",
            "errors": error.messages,
        }, HTTPStatus.BAD_REQUEST
    except IntegrityError as e:
        logger.error(str(e))
        return {"message": "This role exists"}, HTTPStatus.INTERNAL_SERVER_ERROR
    except Exception as e:
        logger.error(str(e))
        return {"message": "Failed to add role"}, HTTPStatus.INTERNAL_SERVER_ERROR
    return {
        "id": role.id,
        "name": role.name,
    }, HTTPStatus.CREATED


@roles_bp.patch("/update/<uuid:id>")
@jwt_required()
@auth_required(["AccessControle"])
def update_role(id):
    """
    ---
    patch:
      summary: Изменить роль
      security:
       - AccessToken: []
      requestBody:
        content:
          application/json:
            schema: RoleNameSchema
      parameters:
        - name: role_id
          in: path
          description: id роли
          required: true
          schema: RoleIdSchema
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
        data = role_name_schema.load(request.json)
        name = data.get("name")
        role = RoleService.get_role(id)
        RoleService.update_role(role, name)
        return {
            "id": role.id,
            "name": role.name,
        }, 200
    except ValidationError as error:
        return {
            "message": "Validation error",
            "errors": error.messages,
        }, HTTPStatus.BAD_REQUEST
    except NotFound as e:
        logger.error(str(e))
        return {"message": "Role not found"}, HTTPStatus.NOT_FOUND
    except Exception as e:
        logger.error(str(e))
        return {"message": "Failed to update role"}, HTTPStatus.INTERNAL_SERVER_ERROR


@roles_bp.delete("/delete/<id>")
@jwt_required()
@auth_required(["AccessControle"])
def delete_role(id):
    """
    ---
    delete:
      summary: Удалить роль
      security:
       - AccessToken: []
      parameters:
        - name: role_id
          in: path
          description: id роли
          required: true
          schema: RoleIdSchema
      responses:
        '202':
          description: ACCEPTED
          content:
            application/json:
              schema: SuccessResponseSchema
      tags:
        - Role
    """
    try:
        role = RoleService.get_role(id)
        RoleService.delete_role(role)
        return {"message": "Role deleted successfully"}, HTTPStatus.ACCEPTED
    except NotFound as e:
        logger.error(str(e))
        return {"message": "Not found"}, HTTPStatus.NOT_FOUND
    except Exception as e:
        logger.error(str(e))
        return {"message": "Failed to delete role"}, HTTPStatus.INTERNAL_SERVER_ERROR


@roles_bp.get("/all")
@jwt_required()
@auth_required(["AccessControle"])
def get_all():
    """
    ---
    get:
      summary: Получить все роли
      security:
       - AccessToken: []
      responses:
        '200':
          description: SUCCESS
          content:
            application/json:
              schema: RoleSchema
      tags:
        - Role
    """
    try:
        roles = RoleService.get_all()
        return role_schema.dump(roles, many=True), HTTPStatus.OK
    except NotFound as e:
        logger.error(str(e))
        return {"message": "Not found"}, HTTPStatus.NOT_FOUND
    except Exception as e:
        logger.error(str(e))
        return {"message": "Failed"}, HTTPStatus.INTERNAL_SERVER_ERROR


@roles_bp.post("/<uuid:id>/AddPermissions")
@jwt_required()
@auth_required(["AccessControle"])
def add_role_permissions(id):
    """
    ---
    post:
      summary: Дать разрешение для роли
      security:
       - AccessToken: []
      requestBody:
        content:
          application/json:
            schema: PermissionIdSchema
      parameters:
        - name: role_id
          in: path
          description: id роли
          required: true
          schema: RoleIdSchema
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
        role_id = id
        data = permission_schema.load(request.json)
        permission_id = data.get("permission_id")
        role_permission = RolesPermissions(role_id=role_id, permission_id=permission_id)
        RolePermissionService.add_role_permission(role_permission)
    except ValidationError as error:
        return {
            "message": "Validation error",
            "errors": error.messages,
        }, HTTPStatus.BAD_REQUEST
    except IntegrityError as e:
        logger.error(str(e))
        return {
            "message": "This perm has already been assigned to the role"
        }, HTTPStatus.INTERNAL_SERVER_ERROR
    except Exception as e:
        logger.error(str(e))
        return {
            "message": "Failed to assign a perm to a role"
        }, HTTPStatus.INTERNAL_SERVER_ERROR
    return {
        "message": "The perm was assigned to the role successfully",
    }, 201


@roles_bp.delete("/<uuid:id>/DeletePermissions")
@jwt_required()
@auth_required(["AccessControle"])
def delete_role_permission(id):
    """
    ---
    delete:
      summary: Отобрать разрешение у роли
      security:
       - AccessToken: []
      requestBody:
        content:
          application/json:
            schema: PermissionIdSchema
      parameters:
        - name: role_id
          in: path
          description: id роли
          required: true
          schema: RoleIdSchema
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
        role_id = id
        data = permission_schema.load(request.json)
        permission_id = data.get("permission_id")
        role_permission = RolePermissionService.get_role_permission(
            role_id=role_id, permission_id=permission_id
        )
        if role_permission:
            RolePermissionService.delete_role_permission(role_permission)
            return {
                "message": "Permission's role was revoked successfully"
            }, HTTPStatus.ACCEPTED
    except ValidationError as error:
        return {
            "message": "Validation error",
            "errors": error.messages,
        }, HTTPStatus.BAD_REQUEST
    except Exception as e:
        logger.error(str(e))
        return {
            "message": "Failed to delete a perm to a role"
        }, HTTPStatus.INTERNAL_SERVER_ERROR
    return {"message": "No role no perm"}, HTTPStatus.BAD_REQUEST
