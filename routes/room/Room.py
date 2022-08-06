from flask import Blueprint, jsonify, request, send_from_directory
from os import getcwd, mkdir, path, makedirs
import errno

# Entities
from models.entities.Room import Room
# Models
from models.RoomModel import RoomModel


PATH_FILE = getcwd() + "/files/"

main = Blueprint('room_blueprint', __name__)


@main.route('/add-room', methods=['POST'])
def add_room():
    try:
        name = request.json['name']
        descriptionShort = request.json['descriptionShort']
        descriptionLarge = request.json['descriptionLarge']
        price = request.json['price']

        room = Room(name, descriptionShort, descriptionLarge, price)

        affected_rows = RoomModel.register(room)

        if affected_rows >= 1:
            return jsonify(statusCode=200,
                           data=room), 200
        else:
            return jsonify(statusCode=500, message='Failed to add room', method='add_room'), 500

    except Exception as ex:
        return jsonify(statusCode=500, message=str(ex), method='register'), 500


@main.route('/add-images-room', methods=['POST'])
def add_images_room():
    try:
        file = request.files['file']
        name = request.form['name']
        descriptionShort = request.form['descriptionShort']
        descriptionLarge = request.form['descriptionLarge']
        price = request.form['price']
        code = request.form['code']

        path_new = PATH_FILE.replace("\\", "/")
        

        if path.isdir(path_new + code) == False:
            makedirs(path_new + code)

        path_save_image = path_new + code + "/" + file.filename

        file.save(path_save_image)

        room = Room(name, descriptionShort, descriptionLarge, price, code)

        return jsonify(statusCode=200,
                           data=path_save_image), 200

        """ affected_rows = RoomModel.register(room)

        if affected_rows >= 1:
            return jsonify(statusCode=200,
                           data=room), 200
        else:
            return jsonify(statusCode=500, message='Failed to add room', method='add_room'), 500 """

    except Exception or OSError as ex:
        if ex.errno != errno.EEXIST:
            raise
        return jsonify(statusCode=500, message=str(ex), method='register'), 500


@main.route('/get-image', methods=['GET'])
def get_image():
    path_new = PATH_FILE.replace("\\", "/")
    return send_from_directory(path_new, path="/abcsplash.jpg", as_attachment=False)

