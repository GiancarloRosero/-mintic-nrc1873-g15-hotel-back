from flask import Blueprint, jsonify, request, Response

# Entities
from models.entities.User import User
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


@main.route('/register', methods=['POST'])
def register():
    try:
        fullName = request.json['fullName']
        document = request.json['document']
        email = request.json['email']
        password = request.json['password']

        user = User(fullName, document, email, password)

        affected_rows = UserModel.register_user(user)

        if affected_rows == 1:
            return jsonify(statusCode=200,
                       data=user.email), 200
        else:
            return jsonify({'message': 'Error on insert'}), 500

        
    except Exception as ex:
        return jsonify({'message': str(ex), 'method': 'register'}), 500
