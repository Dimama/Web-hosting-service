from flask_restful import Resource, reqparse, current_app
from application.auth_connector import AuthConnector
from application.const import AUTH_SERVICE_ADDRESS as auth_addr
from flask import request


class AppLogin(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('client_id', required=True,
                                     help='This field cannot be blank')
        self.parser.add_argument('redirect_uri', required=True,
                                     help='This field cannot be blank')
        self.parser.add_argument('response_type', required=True,
                                 help='This field cannot be blank')
        self.parser.add_argument('login', required=True,
                                 help='This field cannot be blank')
        self.parser.add_argument('password', required=True,
                                 help='This field cannot be blank')
        super(AppLogin, self).__init__()

    def get(self):

        current_app.logger.info("GET: {}".format(request.full_path))

        args = self.parser.parse_args()

        if args['response_type'] != 'code':
            return {'message': 'Only code auth allowed'}, 400

        a_conn = AuthConnector(auth_addr)
        status, body = a_conn.get_auth_code(args['client_id'],
                                            args['login'],
                                            args['password'])

        if status == 200:
            return {'message': 'OK'}, 302, {'Location': 'http://{}/?code={}'.format(
                args['redirect_uri'], body['code'])}

        return body, status


class AppToken(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('client_id', required=True,
                                     help='This field cannot be blank')
        self.parser.add_argument('client_secret', required=True,
                                     help='This field cannot be blank')
        self.parser.add_argument('code', required=True,
                                     help='This field cannot be blank')

        super(AppToken, self).__init__()

    def get(self):

        current_app.logger.info("POST: {}".format(request.full_path))

        args = self.parser.parse_args()

        a_conn = AuthConnector(auth_addr)
        status, body = a_conn.get_token_oauth2(args['client_id'],
                                               args['client_secret'],
                                               args['code'])

        return body, status


class AppTokenRefresh(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('refresh_token', required=True,
                                     help='This field cannot be blank')

        super(AppTokenRefresh, self).__init__()

    def get(self):
        current_app.logger.info("GET: {}".format(request.full_path))

        args = self.parser.parse_args()

        a_conn = AuthConnector(auth_addr)
        status, body = a_conn.refresh_token(args['refresh_token'])

        return body, status