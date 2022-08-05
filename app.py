from config import config
from flask import Flask


# Routes
from routes.auth import Auth

app = Flask(__name__)


def page_not_found(error):
    return "<h1>Not found page </h1>", 404


@app.route('/')
def index():
    return 'Health up'


if __name__ == '__main__':
    app.config.from_object(config['development'])

    # Routes
    app.register_blueprint(Auth.main, url_prefix='/auth')

    # Errors
    app.register_error_handler(404, page_not_found)
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
