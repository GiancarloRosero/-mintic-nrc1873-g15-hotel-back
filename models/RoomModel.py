from flask import jsonify
from database.db import get_connection
from werkzeug.security import check_password_hash


class RoomModel():

    @classmethod
    def register(self, room):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO public.room (name, description_short, description_large, price, code)
                    VALUES (%s, %s, %s, %s, %s)""", (room.name, room.descriptionShort, room.descriptionLarge, room.price, room.code,))
                affected_rows = cursor.rowcount
                connection.commit()

            connection.close()
            return affected_rows
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def add_images(self, code, path_save_image, mimetype):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute(
                    """SELECT id FROM public.room where code = %s """, (code,))
                result = cursor.fetchone()

                if result != None:
                    cursor.execute(
                        """INSERT INTO public.images_room (room_id, url, mimetype)
                    VALUES (%s, %s, %s)""", (result[0], path_save_image, mimetype,))
                affected_rows = cursor.rowcount
                connection.commit()

            connection.close()
            return affected_rows
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_all_names_images(self, code):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute(
                    """SELECT url FROM public.room r
                    JOIN public.images_room ir ON r.id = ir.room_id
                    WHERE r.code = %s """, (code,))
                result = cursor.fetchall()

            connection.close()
            return result
        except Exception as ex:
            raise Exception(ex)
