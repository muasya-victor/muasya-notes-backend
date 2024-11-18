from flask import Blueprint
from flask_restful import Api

from users.resources.list_create import UsersListCreate

users_bp = Blueprint('users', __name__)

api = Api(users_bp)

api.add_resource(UsersListCreate, '/')
