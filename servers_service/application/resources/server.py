from flask_restful import Resource, reqparse
from application.models.models import ServerModel


class Server(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('page', type=int, required=True,
                                   help='No pagination page')
        self.reqparse.add_argument('size', type=int, choices=[1, 2, 3, 4, 5],
                                   default=5, help='Incorrect size per page')
        super(Server, self).__init__()

    def get(self, server_id=None):
        """
        Method to process get responses for server resources

        :param server_id: id of server
        :return: (response data in json, response status code)
        """
        # TODO: add logging here

        if server_id is None:
            args = self.reqparse.parse_args()

            page = args['page']
            per_page = args['size']
            objects = ServerModel.get_servers_with_pagination(page, per_page)

            if not objects:
                return {'message': 'servers not found'}, 404
            else:
                return {'servers': [o.to_json() for o in objects]}, 200

        else:
            res = ServerModel.get_full_server_info_by_id(server_id)
            if res is None:
                return {'message': 'server not found'}, 404
            else:
                resp_body = res[0].to_json()
                resp_body.update(res[1].to_json())
                return {'server info': resp_body}, 200
