import requests


class ServiceConnector(object):
    """
    Base class to connect with other services
    """

    def __init__(self, base_url):
        self.base_url = base_url

    def send_get_request(self, url):
        """
        Send get request to url param

        :param url: second part of destination url
        :return: (response code, response data in json)
        """
        r = requests.get(self.base_url + url)
        return r.status_code, r.json()

    def send_post_request(self, url, body):
        """
        Send post request to url param

        :param url: second part of destination url
        :param body: request body in json
        :return: (response code, response data in json)
        """

        r = requests.post(self.base_url + url, json=body)
        return r.status_code, r.json()

    def send_delete_request(self, url):
        """
        Send delete request to url param

        :param url: second part of destination url
        :return: (response code, response data in json)
        """

        r = requests.delete(self.base_url + url)
        return r.status_code, r.json()