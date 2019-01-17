from .service_connector import ServiceConnector
from flask_restful import current_app


class AuthConnector(ServiceConnector):
    """
    Class to connect with Auth Service
    """

    def check_token(self, token):

        code, body = self.send_get_request('/auth/check?token={}'.format(token))
        current_app.logger.debug("Response from auth: {}, {}".format(body, code))

        return code, body

    def refresh_token(self, refresh_token):

        code, body = self.send_get_request('/auth/refresh?refresh_token={}'.
                                           format(refresh_token))
        current_app.logger.debug("Response from auth: {}, {}".format(body, code))

        return code, body

    def get_token(self, login, password):

        code, body = self.send_get_request('/auth/login?login={}&password={}'.
                                           format(login, password))
        current_app.logger.debug("Response from auth: {}, {}".format(body, code))

        return code, body
