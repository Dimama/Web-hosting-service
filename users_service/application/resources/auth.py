from flask_restful import Resource
from flask import current_app, request
from flask_jwt_extended import create_access_token
import base64


class Auth(Resource):

    def get(self):

        current_app.logger.info('GET: {}'.format(request.full_path))

        try:
            auth_header_b64 = request.headers['Authorization'].split()[-1]
        except KeyError:
            return {'message': 'Authorization Header not found'}, 400
        else:
            try:
                auth_header = base64.b64decode(auth_header_b64).decode()
            except Exception:  # decode exceptions
                return {'message': 'Bad header value'}, 400

            if auth_header == current_app.config['GW-SECRET']:
                token = create_access_token(identity=None)
                return {'message': 'OK', 'token': token}, 200
            else:
                return {'message': 'wrong token'}, 401
