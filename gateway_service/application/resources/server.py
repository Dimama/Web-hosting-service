from flask_restful import Resource
from flask import jsonify


class Server(Resource):
    def get(self, server_id=None):
        if server_id is None:
            # response to servers_service to get all configurations
            # 400 - bad request
            # 200 - ok
            return jsonify({"method": "get"})
        else:
            # response to servers_service to get config by id
            # 400 - bad requset
            # 200 - ok
            # 404 - resource not found
            return jsonify({"server_id": server_id, "method": "get"})
