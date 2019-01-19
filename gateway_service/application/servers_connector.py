from .service_connector import ServiceConnector
from flask_restful import current_app


class ServersConnector(ServiceConnector):
    """
    Class to connect with Servers Service
    """
    def get_servers_with_pag(self, page, size):
        """
        Method to get info about servers using pagination

        :param page: page number
        :param size: count elements per page
        :return: (response code, response data in json)
        """

        url = "/server?page={}&size={}".format(page, size)
        return self.send_get_request(url, with_token=True)

    def get_servers(self):
        """
        Method to get info about all servers

        :return: (response code, response data in json)
        """

        url = "/server".format()
        return self.send_get_request(url)

    def get_server_by_id(self, server_id):
        """
        Method to get info about server with server_id

        :param server_id: id of server which need to get
        :return: (response code, response data in json)
        """

        url = "/server/{}".format(server_id)
        return self.send_get_request(url)

    def get_server_available_count_and_price(self, server_id):
        """
        Method to get count of available servers with server_id and server price
        note:  get full info about server but take only available count and price

        :param server_id: id of server whose count need to get
        :return: (response code, response data in json)
        """

        url = "/server/{}".format(server_id)

        code, body = self.send_get_request(url, with_token=True)

        current_app.logger.debug("Response from servers: {}, {}".format(body, code))

        if code == 404:
            return code, body
        if body['server info']['count'] == 0:
            return 422, {'message': 'no available servers'}

        return code, {'count': body['server info']['count'],
                      'price': body['server info']['price']}

    def change_server_available(self, server_id, decrease=True):
        """
        Method to change available count of server

        :param server_id: id of server whose count need to change
        :param decrease: True - decrease available, False - increase
        :return: (response code, response data in json)
        """

        url = '/server/{}'.format(server_id)

        delta = -1 if decrease else 1
        code, body = self.send_put_request(url, {'delta': delta}, with_token=True)

        current_app.logger.debug("Response from servers: {}, {}".format(body, code))

        if code == 404 or code == 400:
            return code, body

        return code, {'message': 'server available count updated'}

