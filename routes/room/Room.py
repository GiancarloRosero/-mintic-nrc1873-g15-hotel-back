from flask import Blueprint, jsonify, request, send_from_directory, current_app
from os import path, makedirs
import errno

# Entities
from models.entities.Room import Room
from models.entities.Comment import Comment
from models.entities.Reserve import Reserve
# Models
from models.RoomModel import RoomModel


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'png', 'bmp'])

PATH_FILE = path.abspath(path.dirname(__file__))
PATH_FILE_NEW = PATH_FILE.replace("\\", "/")


main = Blueprint('room_blueprint', __name__)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@main.route('/add-room', methods=['POST'])
def add_room():
    try:
        name = request.json['name']
        descriptionShort = request.json['descriptionShort']
        descriptionLarge = request.json['descriptionLarge']
        price = request.json['price']
        code = request.json['code']

        room = Room(name, descriptionShort, descriptionLarge, price, code, 5)

        affected_rows = RoomModel.register(room)

        if affected_rows >= 1:
            return jsonify(status=200,
                           data=room.code), 200
        else:
            return jsonify(status=500, message='Failed to add room', method='add_room'), 500

    except Exception as ex:
        return jsonify(status=500, message=str(ex), method='add-room'), 500


@main.route('/add-images-room', methods=['POST'])
def add_images_room():
    try:
        file = request.files['file']
        code = request.form['code']

        if not allowed_file(file.filename):
            return jsonify(status=500, message='Extension image invalid', method='add_room'), 500

        if path.isdir(PATH_FILE_NEW + "/" + current_app.config['UPLOADED_FOLDER']+"/"+code) == False:
            makedirs(PATH_FILE_NEW+"/" +
                     current_app.config['UPLOADED_FOLDER']+"/"+code)

        path_save_image = PATH_FILE_NEW + "/" + \
            current_app.config['UPLOADED_FOLDER']+code+"/" + file.filename

        file.save(path.join(
            PATH_FILE_NEW, current_app.config['UPLOADED_FOLDER']+code+"/", file.filename))

        affected_rows = RoomModel.add_images(
            code, code + "/" + file.filename, file.mimetype)

        if affected_rows >= 1:
            return jsonify(status=200, data=path_save_image), 200
        else:
            return jsonify(status=500, message='Failed to add image', method='add_images_room'), 500

    except Exception or OSError as ex:
        if ex.errno != errno.EEXIST:
            raise
        return jsonify(status=500, message=str(ex), method='add-images-room'), 500


@main.route('/get-all-images/files/<roomCode>', methods=['GET'])
def get_all_names_images(roomCode):
    urlImagesRoom = []
    for path_img in RoomModel.get_all_names_images(roomCode):
        urlImagesRoom.append(path_img[0])

    return jsonify(status=200, message='Get url images success', data=urlImagesRoom), 200


@main.route('/get-image/<roomCode>/<image>', methods=['GET'])
def get_all_images(roomCode, image):
    return send_from_directory(PATH_FILE_NEW+"/"+current_app.config['UPLOADED_FOLDER'], path=roomCode + "/"+image, as_attachment=False)


@main.route('/get-all-rooms', methods=['GET'])
def get_all_rooms():
    return jsonify(status=200, message='Get rooms success', data=RoomModel.get_all_rooms()), 200


@main.route('/get-room-detail/<roomCode>', methods=['GET'])
def get_room_detail(roomCode):
    return jsonify(status=200, message='Get detail room success', data=RoomModel.get_room_detail(roomCode)), 200


@main.route('/can-add-comment/<userId>/<roomCode>', methods=['GET'])
def can_add_comment(userId, roomCode):
    result = RoomModel.can_add_comment(userId, roomCode)
    if len(result) > 0 :
        return jsonify(status=200, message='You can add comments', data=result[0]), 200
    else:
        return jsonify(status=406, message='Can not add comments', data=result), 200

@main.route('/add-room-comment', methods=['POST'])
def add_room_comment():
    try:
        userId = request.json['userId']
        roomCode = request.json['roomCode']
        score = request.json['score']
        comment = request.json['comment']

        comment = Comment(userId, roomCode, score, comment)

        affected_rows = RoomModel.add_room_comment(comment)

        if affected_rows == 1:
            return jsonify(status=200, data=comment.userId), 200
        else:
            return jsonify(status=500, message='Failed to add comment', method='add_room_comment'), 500

    except Exception as ex:
        return jsonify(status=500, message=str(ex), method='add-room-comment'), 500


@main.route('/get-room-comments/<roomCode>', methods=['GET'])
def get_room_comments(roomCode):
    return jsonify(status=200, message='Get comments room success', data=RoomModel.get_room_comments(roomCode)), 200


@main.route('/reserve', methods=['POST'])
def reserve():
    try:
        userId = request.json['userId']
        roomCode = request.json['roomCode']
        startDate = request.json['startDate']
        endDate = request.json['endDate']

        reserve = Reserve(userId, roomCode, startDate, endDate)

        affected_rows = RoomModel.reserve(reserve)

        if affected_rows == 1:
            return jsonify(status=200, data=reserve.userId), 200
        elif affected_rows == 0:
            return jsonify(status=406, message='Not available', method='reserve'), 200
        else:
            return jsonify(status=500, message='Failed to reserve', method='reserve'), 500

    except Exception as ex:
        return jsonify(status=500, message=str(ex), method='reserve'), 500
