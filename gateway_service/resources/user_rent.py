from flask_restful import Resource, reqparse
from flask import jsonify


class UserRent(Resource):
    def get(self, user_id):
        return jsonify({"id": user_id, "method": "get"})

    def post(self, user_id):
        return jsonify({"id": user_id, "method": "post"})

    def delete(self, user_id, rent_id):
        return jsonify({"user_id": user_id, "rent_id": rent_id,
                        "method": "delete"})