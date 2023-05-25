from flask import Blueprint, request
from src.models.roles import Role
from src.services.roles import RoleService

roles_bp = Blueprint('roles', __name__)


@roles_bp.post('/create')
def add_role():
    data = request.json
    if data:
        role = Role(name=data['name'])
        RoleService.add_role(role)
    return {'message': 'Role created successfully'}


@roles_bp.delete('/delete/<name>')
def delete_role(name):
    message = RoleService.delete_role(name)
    return {'message': message}


@roles_bp.route('/get/<name>', methods=['GET'])
def get_role(name):
    role = RoleService.get_role(name)
    if role:
        return {'name': role.name}
    else:
        return {'message': f'Role {name} not found'}, 404
