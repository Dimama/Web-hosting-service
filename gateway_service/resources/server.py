from flask_restful import Resource
from flask import jsonify


class Server(Resource):
    def get(self, server_id=None):
        if server_id is None:
            return jsonify({"method": "get"})
        else:
            return jsonify({"server_id": server_id, "method": "get"})
