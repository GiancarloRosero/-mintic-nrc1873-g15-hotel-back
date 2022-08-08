from fileinput import filename
from flask import Blueprint, jsonify, request, send_from_directory, Response, send_file, url_for, current_app
from os import getcwd, listdir, mkdir, path, makedirs
import errno
import io

# Entities
from models.entities.Room import Room
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

        room = Room(name, descriptionShort, descriptionLarge, price, code)

        affected_rows = RoomModel.register(room)

        if affected_rows >= 1:
            return jsonify(status=200,
                           data=room.code), 200
        else:
            return jsonify(status=500, message='Failed to add room', method='add_room'), 500

    except Exception as ex:
        return jsonify(status=500, message=str(ex), method='add room'), 500


@main.route('/add-images-room', methods=['POST'])
def add_images_room():
    try:
        file = request.files['file']
        code = request.form['code']

        if not allowed_file(file.filename):
            return jsonify(status=500, message='Extension image invalid', method='add_room'), 500

        if path.isdir(PATH_FILE_NEW + "/" + current_app.config['UPLOADED_FOLDER']+"/"+code) == False:
            makedirs(PATH_FILE_NEW+"/"+current_app.config['UPLOADED_FOLDER']+"/"+code)

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
    print(roomCode)
    return send_from_directory(PATH_FILE_NEW+"/"+current_app.config['UPLOADED_FOLDER'], path=roomCode + "/"+image, as_attachment=False)
