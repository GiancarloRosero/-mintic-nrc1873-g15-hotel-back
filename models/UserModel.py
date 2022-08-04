import imp
from multiprocessing import connection
from database.db import get_connection
from .entities.User import User

class UserModel():

    @classmethod
    def login_user(self, email):
        try:
            connection = get_connection()
            users = []

            with connection.cursor() as cursor:
                cursor.execute("""SELECT id, fullName, document, email FROM public.user where email = %s """, (email,))
                resultset = cursor.fetchall()

                for row in resultset:
                    user = User(row[0], row[1], row[2], row[3], "")
                    users.append(user.to_JSON())

            connection.close()
            return users
        except Exception as ex:
            raise Exception(ex)