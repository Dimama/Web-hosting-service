from flask import Flask
from application.const import DB_URI
from flask_restful import Api
from .database import db
# import resource


def create_app(testing_mode=False):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % DB_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    if not testing_mode:
        db.init_app(app)

        with app.test_request_context():
            db.create_all()

    api = Api(app)
    # add resource to auth

    return app

