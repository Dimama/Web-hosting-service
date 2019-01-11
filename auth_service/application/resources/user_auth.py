from flask_restful import Resource, reqparse
from application.models.models import UserModel


class UserLogin(Resource):

    def __init__(self):
        self.put_parser = reqparse.RequestParser()
        self.put_parser.add_argument('login', required=True, location='json',
                                     help='This field cannot be blank')
        self.put_parser.add_argument('password', required=True, location='json',
                                     help='This field cannot be blank')
        super(UserLogin, self).__init__()

    def post(self):

        args = self.put_parser.parse_args()

        current_user = UserModel.find_by_login(args['login'])

        if not current_user:
            return {'message': 'user not found'}, 404

        if UserModel.verify_hash(args['password'], current_user.password):
            return {'message': 'OK'}, 200
        else:
            return {'message': 'wrong credentials'}, 401