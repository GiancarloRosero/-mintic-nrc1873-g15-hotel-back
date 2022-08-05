from config import config
from flask import Flask
from flask_cors import CORS, cross_origin


# Routes
from routes.auth import Auth

app = Flask(__name__)
app.config['CORS_HEADERS'] = ['Content-Type']
CORS(app)
cors = CORS(app, resources={r"*": {"origins": "*"}})


def page_not_found(error):
    return "<h1>Not found page </h1>", 404


@app.route('/')
def index():
    return 'Health up'

# Routes
app.register_blueprint(Auth.main, url_prefix='/auth')

# Errors
app.register_error_handler(404, page_not_found)


if __name__ == '__main__':
    app.config.from_object(config['development'])

    app.run()


""" @app.route('/login', methods=['POST'])
def login():
    email = request.json['email']
    data = request.json

    return jsonify(isError=False,
                   message="Success",
                   statusCode=200,
                   data=data), 200


app.run(debug=True, port=5000)
 """
