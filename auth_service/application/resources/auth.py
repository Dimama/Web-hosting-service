from flask_restful import Resource, reqparse
import jwt
from application.models.models import UserModel, UserAppCode
from datetime import datetime, timedelta
from random import randint

from flask import current_app, request


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
                                              timedelta(minutes=1)},
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
            data = jwt.decode(refresh_token, verify=False)
        except (jwt.InvalidTokenError, Exception):
            return {'message': 'Invalid refresh token'}, 401

        app_id = data.get('app', None)
        if app_id:
            try:
                secret = current_app.config['APPS'][app_id][0]
                data = jwt.decode(refresh_token, secret + '_refresh')
                user_id = data['sub']
                access_token = jwt.encode({'sub': user_id,
                                         'app': app_id,
                                         'iat': datetime.utcnow(),
                                         'exp': datetime.utcnow() +
                                                timedelta(minutes=1)},
                                        secret)

                return {'message': 'OK', 'access_token': access_token.decode()}, 200
            except (jwt.InvalidTokenError, Exception):
                current_app.logger.error('Invalid refresh token')
                return {'message': 'Invalid refresh token'}, 401

        try:
            data = jwt.decode(refresh_token, current_app.config['JWT_REFRESH_SECRET'])
            id = data['sub']

            access_token = jwt.encode({'sub': id,
                                       'iat': datetime.utcnow(),
                                       'exp': datetime.utcnow() +
                                              timedelta(minutes=1)},
                                      current_app.config['JWT_ACCESS_SECRET'])

            return {'message': 'OK', 'access_token': access_token.decode()}, 200

        except (jwt.InvalidTokenError, Exception):
            current_app.logger.error('Invalid refresh token')
            return {'message': 'Invalid refresh token'}, 401


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
            data = jwt.decode(token, verify=False)
        except (jwt.InvalidTokenError, Exception):
            return {'message': 'Invalid refresh token'}, 401

        app_id = data.get('app', None)

        if app_id:
            secret = current_app.config['APPS'][app_id][0]
        else:
            secret = current_app.config['JWT_ACCESS_SECRET']

        try:
            data = jwt.decode(token, secret)
            return {'message': 'OK', 'user_id': data['sub']}, 200

        except jwt.ExpiredSignatureError:
            current_app.logger.error('Token Expired')
            return {'message': 'Token expired', 'expired': True}, 401
        except (jwt.InvalidTokenError, Exception):
            current_app.logger.error('Invalid  token')
            return {'message': 'Invalid access token', 'expired': False}, 401


class AppCode(Resource):

    def get(self):

        client_id = request.args['client_id']
        login = request.args['login']
        password = request.args['password']

        current_user = UserModel.find_by_login(login)
        if not current_user:
            return {'message': 'wrong credentials'}, 401

        if UserModel.verify_hash(password, current_user.password):
            client_info = current_app.config['APPS'].get(client_id, None)
            if not client_info:
                return {'message': 'application is not registred'}, 404

            code = randint(100, 100000)
            client_info[1] = code

            record = UserAppCode.find(current_user.id, client_id)
            if not record:
                UserAppCode.create_code_record(code=code,
                                               user_id=current_user.id,
                                               app_id=client_id)
            else:
                UserAppCode.update_code(current_user.id, client_id, code)
            return {'message': 'OK', 'code': code}, 200
        else:
            return {'message': 'wrong credentials'}, 401


class AppToken(Resource):

    def get(self):

        client_id = request.args['client_id']
        secret = request.args['client_secret']
        code = request.args['code']

        client_info = current_app.config['APPS'].get(client_id, None)
        if not client_info:
            return {'message': 'application is not registred'}, 404

        if client_info[0] != secret:
            return {'message': 'Incorrect secret'}, 401

        record = UserAppCode.find_by_code(code)
        if not record:
            return {'message': 'App unauthorized'}, 401

        access_token = jwt.encode({'sub': record.user_id,
                                   'app': client_id,
                                   'iat': datetime.utcnow(),
                                   'exp': datetime.utcnow() +
                                          timedelta(minutes=1)},
                                  client_info[0])

        refresh_token = jwt.encode({'sub': record.user_id, 'app': client_id},
                                   client_info[0]+'_refresh')

        return {
                   'message': 'OK',
                   'access_token': access_token.decode(),
                   'refresh_token': refresh_token.decode()
               }, 200

