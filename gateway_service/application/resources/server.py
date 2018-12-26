from flask_restful import Resource, reqparse, current_app
from application.servers_connector import ServersConnector
from application.const import SERVERS_SERVICE_ADDRESS as addr
from flask import request


class Server(Resource):
    """
    Class to work with Server Resource
    """
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('page', type=int, required=False, default=0,
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

        current_app.logger.info("GET: {}".format(request.full_path))

        connector = ServersConnector(addr)
        if server_id is None:
            # response to servers_service to get all configurations
            args = self.reqparse.parse_args()
            page, size = args['page'], args['size']

            if page == 0:
                status, body = connector.get_servers()
            else:
                status, body = connector.get_servers_with_pag(page, size)
        else:
            # response to servers_service to get config by id
            status, body = connector.get_server_by_id(server_id)

        current_app.logger.debug("Response from servers: {}, {}".format(body,
                                                                        status))
        return body, status
