from flask import Flask, Response
from flask.json import jsonify

app = Flask(__name__)


@app.route('/login', methods=['GET'])
def login():
    #email = request.json['email']

    return {'message': 'Bien'}