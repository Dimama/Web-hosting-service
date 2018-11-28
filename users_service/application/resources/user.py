from flask_restful import Resource, reqparse
from application.models.models import UserModel, UserBillsModel
from flask import current_app, request


class User(Resource):
    def __init__(self):
        self.put_parser = reqparse.RequestParser()
        self.put_parser.add_argument('price', type=float, required=True,
                                     location='json', help="price is not set")
        super(User, self).__init__()

    def get(self, user_id):
        """
        Method to process get responses for user resources

        :param user_id: id of user
        :return: (response data in json, response status code)
        """

        current_app.logger.info("GET: {}".format(request.full_path))

        res = UserModel.get_user_info_by_id(user_id)
        if res is None:
            current_app.logger.warn("Resource not found")
            return {'message': 'user not found'}, 404
        else:
            resp_body = res[0].to_json()
            resp_body.update(res[1].to_json())
            return {'user info': resp_body}, 200

    def put(self, user_id):
        """
        Method to process put responses for user resources

        :param user_id: id of user
        :return: (response data in json, response status code)
        """

        current_app.logger.info("PUT: {}".format(request.full_path))

        args = self.put_parser.parse_args()
        updated_bill = UserBillsModel.decrease_user_bill(user_id, args['price'])

        # may be check on 404 ?

        return {'bill': updated_bill}, 200
