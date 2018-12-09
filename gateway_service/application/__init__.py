from flask import Flask
from flask_restful import Api
from application.resources.server import Server
from application.resources.user_rent import UserRent
import logging
from logging.handlers import RotatingFileHandler


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    api = Api(app)
    api.add_resource(Server, '/server',
                     '/server/<int:server_id>')
    api.add_resource(UserRent, '/user/<int:user_id>/rent',
                     '/user/<int:user_id>/rent/<int:rent_id>')

    handler = logging.handlers.RotatingFileHandler(
        'gateway.log',
        maxBytes=1024*100,
        backupCount=5)

    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(filename)s: %(message)s')
    handler.setFormatter(formatter)
    app.logger.setLevel(logging.DEBUG)
    app.logger.addHandler(handler)

    return app
