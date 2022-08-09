from flask import jsonify
from database.db import get_connection
from .entities.User import User
from werkzeug.security import check_password_hash
import json

class UserModel2():

    @classmethod
    def listUserModel():
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute(
                    """SELECT * FROM public.user""")
                result = cursor.fetchall()
                jsonObj = json.dumps(result)

                response = jsonify(status=401, message='failed'), 401
                if result != None and result > 1:
                    response = jsonify(
                        status=200, message='list of users', result=jsonObj), 200
                print(jsonObj)
            connection.close()
            return response
        except Exception as ex:
            raise Exception(ex)
