from flask import Flask
from application.const import DB_URI
from flask_restful import Api
from .database import db
from application.resources.user_auth import UserLogin, TokenRefresh, TokenCheck
import datetime


def create_app(testing_mode=False):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % DB_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['JWT_ACCESS_SECRET'] = 'jwt-access-secret'
    app.config['JWT_REFRESH_SECRET'] = 'jwt-refresh-secret'

    if not testing_mode:
        db.init_app(app)

        with app.test_request_context():
            db.create_all()

    api = Api(app)
    api.add_resource(UserLogin, '/auth/login')
    api.add_resource(TokenRefresh, '/auth/refresh')
    api.add_resource(TokenCheck, '/auth/check')

    return app

