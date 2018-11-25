from .service_connector import ServiceConnector


class ServersConnector(ServiceConnector):
    """
    Class to connect with Servers Service
    """
    def get_servers(self, page, size):
        """
        Method to get info about all servers using pagination

        :param page: page number
        :param size: count elements per page
        :return: (response code, response data in json)
        """

        url = "/server?page={}&size={}".format(page, size)
        return self.send_get_request(url)

    def get_server_by_id(self, server_id):
        """
        Method to get info about server with server_id

        :param server_id: id of server which need to get
        :return: (response code, response data in json)
        """

        url = "/server/{}".format(server_id)
        return self.send_get_request(url)
