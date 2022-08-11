from flask import Blueprint, jsonify, request

# Entities
from models.entities.User import User
# Models
from models.UserModel import UserModel

main = Blueprint('user_blueprint', __name__)


@main.route('/delete-user', methods=['POST'])
def delete_user():
    try:
        id = request.json['id']

        affected_rows = UserModel.delete_user(id)

        if affected_rows == 1:
            return jsonify(status=200, data=id), 200
        else:
            return jsonify(status=500, message='Failed to delete user', method='delete_user'), 500

    except Exception as ex:
        return jsonify(status=500, message=str(ex), method='delete-user'), 500


@main.route('/get-all-users-from-admin', methods=['GET'])
def get_all_users_from_admin():
    return jsonify(status=200, message='Get users success admin', data=UserModel.get_all_users_from_admin()), 200


@main.route('/get-all-users-from-superadmin', methods=['GET'])
def get_all_users_from_superadmin():
    return jsonify(status=200, message='Get users success superadmin', data=UserModel.get_all_users_from_superadmin()), 200
