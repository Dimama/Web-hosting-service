from flask_restful import Resource, reqparse
from application.models.models import ServerModel, ServerInfoModel
from flask import current_app, request
from application.exceptions import NoServerException


class Server(Resource):
    def __init__(self):
        self.get_reqparser = reqparse.RequestParser()
        self.get_reqparser.add_argument('page', type=int, required=False, default=0,
                                   help='No pagination page')
        self.get_reqparser.add_argument('size', type=int, choices=[1, 2, 3, 4, 5],
                                   default=5, help='Incorrect size per page')

        self.put_reqparser = reqparse.RequestParser()
        self.put_reqparser.add_argument('delta', type=int, required=True,
                                     choices=[1, -1], location='json',
                                     help="delta is not set or incorrect")

        super(Server, self).__init__()

    def get(self, server_id=None):
        """
        Method to process get responses for server resources

        :param server_id: id of server
        :return: (response data in json, response status code)
        """

        current_app.logger.info('GET: {}'.format(request.full_path))

        if server_id is None:
            args = self.get_reqparser.parse_args()
            page = args['page']
            per_page = args['size']

            if page == 0:
                objects = ServerModel.get_all_servers()
            else:
                objects = ServerModel.get_servers_with_pagination(page, per_page)

            if not objects:
                current_app.logger.warn("Resource not found")
                return {'message': 'servers not found'}, 404
            else:
                return {'servers': [o.to_json() for o in objects]}, 200

        else:
            res = ServerModel.get_full_server_info_by_id(server_id)
            if res is None:
                current_app.logger.warn("Resource not found")
                return {'message': 'server not found'}, 404
            else:
                resp_body = res[0].to_json()
                resp_body.update(res[1].to_json())
                return {'server info': resp_body}, 200

    def put(self, server_id):
        """
        Method to process put responses for server resources

        :param server_id: id of server
        :return: (response data in json, response status code)
        """

        current_app.logger.info('PUT: {}'.format(request.full_path))
        args = self.put_reqparser.parse_args()

        try:
            updated_count = ServerInfoModel.update_server_available(server_id,
                                                                args['delta'])
        except NoServerException as e:
            current_app.logger.warn(str(e))
            return {'message': str(e)}, 404
        else:
            return {'available count': updated_count}, 200