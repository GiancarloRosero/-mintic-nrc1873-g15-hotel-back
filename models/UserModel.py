from multiprocessing import connection
from database.db import get_connection
from .entities.User import User


class UserModel():

    @classmethod
    def login_user(self, email):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute(
                    """SELECT fullName, document, email FROM public.user where email = %s """, (email,))
                result = cursor.fetchone()

                user = None
                if result != None:
                    user = User(result[0], result[1], result[2], result[3], "")
                    user = user.to_JSON()

            connection.close()
            return user
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
