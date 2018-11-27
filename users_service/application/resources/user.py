from flask_restful import Resource
from application.models.models import UserModel
from flask import current_app, request


class User(Resource):

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
