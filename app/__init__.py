from flask import Blueprint, Flask
from flask_restx import Api
from .main.controllers.assistant_controller import ms_assistant
from .main import psql
from flask_cors import CORS

app = Flask(__name__)

blueprint = Blueprint("api", __name__)

api = Api(
    blueprint,
    title="Assistant Microservice",
    version="1.0",
    description="Assistant Microservice"
)


def route_app():
    api.add_namespace(ms_assistant, path="")


def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})
    app.config.from_pyfile('config.py')
    route_app()

    return app


class PrefixMiddleware(object):

    def __init__(self, app, prefix=''):
        self.app = app
        self.prefix = prefix

    def __call__(self, environ, start_response):
        environ['PATH_INFO'] = environ['PATH_INFO'][len(self.prefix):]
        environ['SCRIPT_NAME'] = self.prefix
        return self.app(environ, start_response)
