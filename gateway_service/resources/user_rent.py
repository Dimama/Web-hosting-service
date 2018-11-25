from flask_restful import Resource, reqparse
from flask import jsonify


class UserRent(Resource):
    def get(self, user_id):
        # add pagination
        # 400 - bad request
        # 200 - ok
        # 404 - not found
        # get configurations for user
        # get configurations from servers_service
        # accamulate data

        return jsonify({"id": user_id, "method": "get"})

    def post(self, user_id):
        # 400 - bad request (validate body data)
        # check user bills (code???)
        # check server available (code???)
        # update user bill
        # update server_availble
        # create rent record and sent record to user (200)
        return jsonify({"id": user_id, "method": "post"})

    def delete(self, user_id, rent_id):
        # 400 - bad request
        # delete rent (404 not found rent)
        # update server available
        # return 204
        return jsonify({"user_id": user_id, "rent_id": rent_id,
                        "method": "delete"})