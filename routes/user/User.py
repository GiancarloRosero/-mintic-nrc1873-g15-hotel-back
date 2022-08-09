from flask import Blueprint, jsonify, request, send_from_directory, current_app
from os import path, makedirs

# Entities
from models.entities.User import User
# Models
from models.UserModel import UserModel

main = Blueprint('user_blueprint', __name__)



@main.route('/get-all-users', methods=['GET'])
def get_all_Users():
    return jsonify(status=200, message='Get Users success', data=UserModel.get_all_users()), 200