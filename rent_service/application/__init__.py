from flask import Flask
from application.const import DB_URI
from .database import db
from flask_restful import Api
import logging
from application.resources.rent import Rent
from logging.handlers import RotatingFileHandler


def create_app(testing_mode=False):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % DB_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    if not testing_mode:
        db.init_app(app)

        with app.test_request_context():
            db.create_all()

    api = Api(app)
    api.add_resource(Rent, '/rent', '/rent/<int:rent_id>',
                     '/user/<int:user_id>/rent/<int:rent_id>',
                     '/user/<int:user_id>/rent')

    handler = logging.handlers.RotatingFileHandler(
        'rent.log',
        maxBytes=1024*100,
        backupCount=5)

    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(filename)s: %(message)s')
    handler.setFormatter(formatter)
    app.logger.setLevel(logging.DEBUG)
    app.logger.addHandler(handler)

    return app
