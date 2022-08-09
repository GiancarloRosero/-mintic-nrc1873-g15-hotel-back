from flask import Blueprint, jsonify

# Entities
from models.entities.User import User
# Models
from models.UserModel import UserModel

main = Blueprint('user_blueprint', __name__)


@main.route('/get-all-users-from-admin', methods=['GET'])
def get_all_users_from_admin():
    return jsonify(status=200, message='Get users success admin', data=UserModel.get_all_users_from_admin()), 200

@main.route('/get-all-users-from-superadmin', methods=['GET'])
def get_all_users_from_superadmin():
    return jsonify(status=200, message='Get users success superadmin', data=UserModel.get_all_users_from_superadmin()), 200
