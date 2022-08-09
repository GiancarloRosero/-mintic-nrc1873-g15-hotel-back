from flask import jsonify
from database.db import get_connection
from .entities.Room import Room, RoomJoin
from .entities.Comment import CommentJoinUser


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

    @classmethod
    def get_all_rooms(self):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute(
                    """SELECT DISTINCT ON (name) name, description_short, description_large,
                    price, code, score, ir.url FROM public.room r JOIN public.images_room ir
                    ON ir.room_id = r.id """)
                result = cursor.fetchall()

            rooms = []
            for room in result:
                rooms.append(
                    RoomJoin(room[0], room[1], room[2], room[3], room[4], room[5], room[6]).to_JSON())

            connection.close()
            return rooms
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_room_detail(self, codeRoom):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute(
                    """SELECT name, description_short, description_large,
                    price, code, score FROM public.room WHERE code = %s """, (codeRoom,))
                result = cursor.fetchone()

                room = Room(result[0], result[1], result[2],
                            result[3], result[4], result[5]).to_JSON()

            connection.close()
            return room
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def add_room_comment(self, comment):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO public.comment (user_id, room_code, score, comment)
                    VALUES (%s, %s, %s, %s)""", (comment.userId, comment.roomCode, comment.score, comment.comment,))
                affected_rows = cursor.rowcount
                connection.commit()

            connection.close()
            return affected_rows
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_room_comments(self, codeRoom):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute(
                    """SELECT user_id, room_code, score, comment, u.fullname
                    FROM public.comment c
                    JOIN public.user u ON u.id = c.user_id
                    WHERE room_code = %s """, (codeRoom,))

                result = cursor.fetchall()

                comments = []
                for comment in result:
                    comments.append(
                        CommentJoinUser(comment[0], comment[1], comment[2], comment[3], comment[4]).to_JSON())

                connection.close()
                return comments
        except Exception as ex:
            raise Exception(ex)
