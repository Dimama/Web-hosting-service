from flask_restful import Resource, reqparse, current_app
from application.auth_connector import AuthConnector
from application.const import AUTH_SERVICE_ADDRESS as auth_addr
from flask import request


class UserLogin(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('login', required=True, location='json',
                                     help='This field cannot be blank')
        self.parser.add_argument('password', required=True, location='json',
                                     help='This field cannot be blank')
        super(UserLogin, self).__init__()

    def post(self):

        current_app.logger.info("POST: {}".format(request.full_path))

        args = self.parser.parse_args()
        login, password = args['login'], args['password']

        a_conn = AuthConnector(auth_addr)
        status, body = a_conn.get_token(login, password)

        return body, status


class TokenRefresh(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('refresh_token', required=True, location='json',
                                     help='This field cannot be blank')

    def post(self):

        current_app.logger.info("POST: {}".format(request.full_path))

        args = self.parser.parse_args()
        refresh_token = args['refresh_token']

        a_conn = AuthConnector(auth_addr)
        status, body = a_conn.refresh_token(refresh_token)

        return body, status