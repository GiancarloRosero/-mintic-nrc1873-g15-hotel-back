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

        if path.isdir(path_new + "/" + current_app.config['UPLOADED_FOLDER']+"/"+code) == False:
            makedirs(path_new+"/"+current_app.config['UPLOADED_FOLDER']+"/"+code)

        path_save_image = path_new + "/" + \
            current_app.config['UPLOADED_FOLDER']+code+"/" + file.filename

        file.save(path.join(
            path_new, current_app.config['UPLOADED_FOLDER']+code+"/", file.filename))

        """ file.save(path.join(current_app.config['UPLOADED_FOLDER'], file.filename)) """

        """ return jsonify(status=200,
                           data=path_save_image), 200 """

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
    valor = []
    path_new = PATH_FILE.replace("\\", "/")
    for path_img in RoomModel.get_all_names_images(roomCode):
        valor.append(path_img)

        """ valor.append(send_from_directory(path_new, path=path_img[0], as_attachment=True)) """
        """ RoomModel.get_all_names_images(roomCode) """
        """"
        with open(path_new+roomCode+path_img, encoding='utf8') as f_obj:
            contents = f_obj.read()
            print(contents
            valor.append(contents) """
    print(valor[0][0])
    print(valor[0][1])
    return url_for('static', filename=valor[0][0])
    """ return send_from_directory(path_new, path="path_img[0]", as_attachment=False) """

    """ return jsonify(status=200, message='Get url images success', data=valor), 200 """


@main.route('/get-all-images/fiiles/<roomCode>', methods=['GET'])
def get_all_images(roomCode):
    path_new = PATH_FILE.replace("\\", "/")
    imageList = listdir('files/'+roomCode)
    imageList = [path_new+roomCode+image for image in imageList]
    """ return send_from_directory(path_new, path="abcf/splash.jpg", as_attachment=False) """
    """ return jsonify(status=200, data=imageList), 200 """
