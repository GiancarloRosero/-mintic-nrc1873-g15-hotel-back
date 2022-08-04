from flask import Blueprint, jsonify, request, Response


# Models
from models.UserModel import UserModel

main = Blueprint('login_blueprint', __name__)

@main.route('/login', methods=['POST'])
def login():
    try:
        email = request.json['email']
        data = request.json
        user = UserModel.login_user(email)
        return jsonify(statusCode=200,
                       data=user), 200
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
