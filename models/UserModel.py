from flask import jsonify
from database.db import get_connection
from .entities.User import User
from werkzeug.security import check_password_hash


class UserModel():

    @classmethod
    def login_user(self, email, password):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute(
                    """SELECT password FROM public.user where email = %s """, (email,))
                result = cursor.fetchone()

                response = jsonify(statusCode=401, message='Login failed, credentials incorrect'), 401
                if result != None and check_password_hash(result[0], password):
                    response = jsonify(statusCode=200, message='Login success'), 200

            connection.close()
            return response
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def register_user(self, user):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO public.user (fullname, document, email, password)
                    VALUES (%s, %s, %s, %s)""", (user.fullName, user.document, user.email, user.password))
                affected_rows = cursor.rowcount
                connection.commit()

            connection.close()
            return affected_rows
        except Exception as ex:
            raise Exception(ex)
