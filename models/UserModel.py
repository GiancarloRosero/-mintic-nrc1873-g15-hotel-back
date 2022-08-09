from flask import jsonify
from database.db import get_connection
from .entities.User import User
from .entities.User import userJoin
from werkzeug.security import check_password_hash


class UserModel():

    @classmethod
    def login_user(self, email, password):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute(
                    """SELECT password, id, rol_id FROM public.user where email = %s """, (email,))
                result = cursor.fetchone()

                response = jsonify(
                    status=401, message='Login failed, credentials incorrect'), 401
                if result != None and check_password_hash(result[0], password):
                    response = jsonify(
                        status=200, message='Login success', id=result[1], rol=result[2]), 200

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


    @classmethod
    def get_all_users(self):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute(
                    """SELECT u.id, u.fullname, u."document", u.email , r."name"  FROM "user" u INNER JOIN "rol" r ON u.rol_id = r.id;""")
                result = cursor.fetchall()

            users = []
            for user in result:
                users.append(
                    userJoin(user[0], user[1], user[2], user[3], user[4]).to_JSON())

            connection.close()
            return users
        except Exception as ex:
            raise Exception(ex)

    # @classmethod
    # def list_user():
    #     try:
    #         connection = get_connection()

    #         with connection.cursor() as cursor:
    #             cursor.execute(
    #                 """SELECT * FROM public.user""")
    #             result = cursor.fetchall()

    #         users = []
    #         for user in result:
    #             users.append(
    #                 userJoin(user[0], user[1], user[2], user[3], user[4], user[5], user[6]).to_JSON())

    #         connection.close()
    #         return users

    #             response = jsonify(status=401, message='failed'), 401
    #             if result != None and result > 1:
    #                 response = jsonify(
    #                     status=200, message='list of users', result=jsonObj), 200
    #             print(jsonObj)
    #         connection.close()
    #         return response
    #     except Exception as ex:
    #         raise Exception(ex)
