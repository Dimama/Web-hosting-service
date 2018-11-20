from flask_restful import Resource, reqparse, abort
from flask import jsonify


class Server(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('page', type=int, required=True, help='No pagination page')
        self.reqparse.add_argument('size', type=int, choices=[1, 2, 3, 4, 5], default=5, help='Incorrect size per page')
        super(Server, self).__init__()

    def get(self, server_id=None):
        if server_id is None:
            args = self.reqparse.parse_args()
            return jsonify({"page": args['page'], "size": args['size']})
        else:
            return jsonify({"server_id": server_id})

