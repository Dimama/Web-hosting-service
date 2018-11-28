from flask import Flask
from application.const import DB_URI
from .database import db
from flask_restful import Api
import logging
from application.resources.user import User
from logging.handlers import RotatingFileHandler


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % DB_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    db.init_app(app)

    with app.test_request_context():
        db.create_all()

    api = Api(app)
    api.add_resource(User, '/user/<int:user_id>')

    handler = logging.handlers.RotatingFileHandler(
        'users.log',
        maxBytes=1024*100,
        backupCount=5)

    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(filename)s: %(message)s')
    handler.setFormatter(formatter)
    app.logger.setLevel(logging.DEBUG)
    app.logger.addHandler(handler)

    return app
