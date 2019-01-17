from flask_restful import Resource, reqparse
import jwt
from application.models.models import UserModel
from datetime import datetime, timedelta

from flask import current_app


class UserLogin(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('login', required=True,
                                     help='This field cannot be blank')
        self.parser.add_argument('password', required=True,
                                     help='This field cannot be blank')
        super(UserLogin, self).__init__()

    def get(self):

        args = self.parser.parse_args()

        current_user = UserModel.find_by_login(args['login'])

        if not current_user:
            return {'message': 'user not found'}, 404

        if UserModel.verify_hash(args['password'], current_user.password):
            access_token = jwt.encode({'sub': current_user.id,
                                       'iat': datetime.utcnow(),
                                       'exp': datetime.utcnow() +
                                              timedelta(minutes=30)},
                                      current_app.config['JWT_ACCESS_SECRET'])

            refresh_token = jwt.encode({'sub': current_user.id},
                                      current_app.config['JWT_REFRESH_SECRET'])

            return {
                    'message': 'OK',
                    'access_token': access_token.decode(),
                    'refresh_token': refresh_token.decode()
                   }, 200
        else:
            return {'message': 'wrong credentials'}, 401


class TokenRefresh(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('refresh_token', required=True,
                                     help='This field cannot be blank')
        super(TokenRefresh, self).__init__()

    def get(self):
        args = self.parser.parse_args()

        refresh_token = args['refresh_token']

        try:
            data = jwt.decode(refresh_token, current_app.config['JWT_REFRESH_SECRET'])
            id = data['sub']

            access_token = jwt.encode({'sub': id,
                                       'iat': datetime.utcnow(),
                                       'exp': datetime.utcnow() +
                                              timedelta(minutes=30)},
                                      current_app.config['JWT_ACCESS_SECRET'])

            return {'message': 'OK', 'access_token': access_token.decode()}, 200

        except (jwt.InvalidTokenError, Exception):
            current_app.logger.error('Invalid refresh token')
            return {'message': 'Invalid access token'}, 401


class TokenCheck(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('token', required=True,
                                     help='This field cannot be blank')
        super(TokenCheck, self).__init__()

    def get(self):

        args = self.parser.parse_args()

        token = args['token']

        try:
            data = jwt.decode(token, current_app.config['JWT_ACCESS_SECRET'])
            return {'message': 'OK', 'user_id': data['sub']}, 200

        except jwt.ExpiredSignatureError:
            current_app.logger.error('Token Expired')
            return {'message': 'Token expired', 'expired': True}, 401
        except (jwt.InvalidTokenError, Exception):
            current_app.logger.error('Invalid  token')
            return {'message': 'Invalid access token', 'expired': False}, 401
