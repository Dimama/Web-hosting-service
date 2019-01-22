from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from application.resources.server import Server
from application.resources.user_rent import UserRent
from application.resources.auth import UserLogin, TokenRefresh
from application.resources.oauth2 import AppLogin, AppToken, AppTokenRefresh
import logging
from logging.handlers import RotatingFileHandler


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    app.config['GW-SECRET'] = 'GATEWAY-SECRET'
    app.config['SERVERS'] = ''
    app.config['USERS'] = ''
    app.config['RENT'] = ''
    app.config['AUTH'] = ''

    cors = CORS(app, resources={r"*": {"origins": "*"}})

    api = Api(app)
    api.add_resource(Server, '/server',
                     '/server/<int:server_id>')
    api.add_resource(UserRent, '/user/<int:user_id>/rent',
                     '/user/<int:user_id>/rent/<int:rent_id>')
    api.add_resource(UserLogin, '/login')
    api.add_resource(TokenRefresh, '/refresh')
    api.add_resource(AppLogin, '/oauth2/code')
    api.add_resource(AppToken, '/oauth2/token')
    api.add_resource(AppTokenRefresh, '/oauth2/refresh')


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
