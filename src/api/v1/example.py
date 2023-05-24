from flask import Blueprint, request

from src.models.users import User
from src.services.example import UsersService

api_bp = Blueprint('api', __name__)


@api_bp.route('/users', methods=['GET'])
def get_users():
    users = UsersService.get_all_users()
    return {'users': [user.to_dict() for user in users]}


@api_bp.route('/create_users', methods=['POST'])
def create_user():
    data = request.json or {}
    user = User(**data)
    UsersService.add_user(user)
    return {'user': user.to_dict()}
