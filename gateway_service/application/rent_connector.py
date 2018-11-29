from .service_connector import ServiceConnector
from flask_restful import current_app


class RentConnector(ServiceConnector):
    """
    Class to connect with Rent service
    """

    def create_rent(self, user_id, server_id, duration):
        """
        Method to create rent in Rent service

        :param user_id:
        :param server_id: id of rent server
        :param duration: duration of rent
        :return: (response code, response data in json)
        """

        code, body = self.send_post_request('/rent', {'user_id': user_id,
                                                      'server_id': server_id,
                                                      'duration': duration})

        current_app.logger.debug("Response from rent: {}, {}".format(body, code))

        # TODO lab 5: check if not created

        return code, {'message': 'rent was created'}
