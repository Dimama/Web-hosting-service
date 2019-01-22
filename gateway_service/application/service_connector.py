import requests
from flask_restful import current_app
from base64 import b64encode


class ServiceConnector(object):
    """
    Base class to connect with other services
    """

    def __init__(self, base_url, service_name=''):
        self.base_url = base_url
        self.service_name = service_name

    def _update_token(self):

        secret = b64encode(current_app.config['GW-SECRET'].encode()).decode()
        headers = {'Authorization': 'Basic ' + secret}

        r = requests.get(self.base_url + '/auth', headers=headers)

        code = r.status_code
        body = r.json()

        if code == 200:
            current_app.logger.info("Successful getting token from " + self.service_name)
            current_app.config[self.service_name] = body['token']
        else:
            current_app.logger.error("Error of getting token from " + self.service_name)

    def _make_headers(self, with_token=False):

        if with_token:
            if not current_app.config[self.service_name]:
                self._update_token()

            headers = {'Authorization':
                           'Bearer ' + current_app.config[self.service_name]}
        else:
            headers = {}

        return headers

    def send_get_request(self, url, with_token=False):
        """
        Send get request to url param

        :param url: second part of destination url
        :param with_token: send request with access token or not
        :return: (response code, response data in json)
        """

        headers = self._make_headers(with_token)

        try:
            r = requests.get(self.base_url + url, headers=headers)
        except requests.exceptions.ConnectionError:
            return 503, {'message': 'service is not available'}

        code = r.status_code
        data = r.json()

        if with_token and code in [400, 401]:
            self._update_token()
            return self.send_get_request(url, with_token=with_token)

        return code, data

    def send_post_request(self, url, body, with_token=False):
        """
        Send post request to url param

        :param url: second part of destination url
        :param body: request body in json
        :param with_token: send request with access token or not
        :return: (response code, response data in json)
        """

        headers = self._make_headers(with_token)

        try:
            r = requests.post(self.base_url + url, json=body, headers=headers)
        except requests.exceptions.ConnectionError:
            return 503, {'message': 'service is not available'}

        code = r.status_code
        data = r.json()

        if with_token and code in [400, 401]:
            self._update_token()
            return self.send_post_request(url, body, with_token=with_token)

        return code, data

    def send_delete_request(self, url, with_token=False):
        """
        Send delete request to url param

        :param url: second part of destination url
        :param with_token: send request with access token or not
        :return: (response code, response data in json)
        """

        headers = self._make_headers(with_token)

        try:
            r = requests.delete(self.base_url + url, headers=headers)
        except requests.exceptions.ConnectionError:
            return 503, {'message': 'service is not available'}

        code = r.status_code

        if with_token and code in [400, 401]:
            self._update_token()
            return self.send_delete_request(url, with_token=with_token)

        if code == 204:
            return code, {'message': 'resource deleted'}

        return code, r.json()

    def send_put_request(self, url, body, with_token=False):
        """
        Send put request to url param

        :param url: second part of destination url
        :param body: request body in json
        :param with_token: send request with access token or not
        :return: (response code, response data in json)
        """

        headers = self._make_headers(with_token)

        try:
            r = requests.put(self.base_url + url, json=body, headers=headers)
        except requests.exceptions.ConnectionError:
            return 503, {'message': 'service is not available'}

        code = r.status_code
        data = r.json()

        if with_token and code in [400, 401]:
            self._update_token()
            return self.send_put_request(url, body, with_token=with_token)

        return code, data