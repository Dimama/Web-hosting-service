from flask_restful import Resource
from flask import jsonify

class User(Resource):
    def get(self, user_id):
        return jsonify({"user_id": user_id, "method": "get"})