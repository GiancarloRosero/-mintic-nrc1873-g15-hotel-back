from flask import Blueprint, jsonify, request, send_from_directory
from os import getcwd, listdir, mkdir, path, makedirs
import errno

# Entities
from models.entities.Room import Room
# Models
from models.RoomModel import RoomModel


ALLOWED_EXTENSIONS = set(['png','jpg','jpeg','png','bmp'])

PATH_FILE = getcwd() + "/files/"

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

        path_new = PATH_FILE.replace("\\", "/")
        

        if path.isdir(path_new + code) == False:
            makedirs(path_new + code)

        path_save_image = path_new + code + "/" + file.filename

        file.save(path_save_image)

        """ return jsonify(status=200,
                           data=path_save_image), 200 """

        affected_rows = RoomModel.add_images(code, path_save_image)

        if affected_rows >= 1:
            return jsonify(status=200, data=path_save_image), 200
        else:
            return jsonify(status=500, message='Failed to add room', method='add_room'), 500

    except Exception or OSError as ex:
        if ex.errno != errno.EEXIST:
            raise
        return jsonify(status=500, message=str(ex), method='register'), 500


@main.route('/get-all-images/files/<roomCode>', methods=['GET'])
def get_all_images(roomCode):
    path_new = PATH_FILE.replace("\\", "/")
    imageList = listdir('/app/files/'+roomCode)
    imageList = [path_new+roomCode+image for image in imageList]
    return jsonify(status=200, data=imageList), 200

