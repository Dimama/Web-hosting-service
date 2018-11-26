from flask_restful import Resource, reqparse
from application.servers_connector import ServersConnector
from application.const import SERVERS_SERVICE_ADDRESS as addr


class Server(Resource):
    """
    Class to work with Server Resource
    """
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

        connector = ServersConnector(addr)
        if server_id is None:
            # response to servers_service to get all configurations
            args = self.reqparse.parse_args()
            page, size = args['page'], args['size']

            status, body = connector.get_servers(page, size)
            print("Response from service: ", body) # DEBUG

        else:
            # response to servers_service to get config by id
            status, body = connector.get_server_by_id(server_id)
            print("Response from service: ", body)  # DEBUG

        return body, status
