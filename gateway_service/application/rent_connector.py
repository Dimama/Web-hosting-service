from .service_connector import ServiceConnector
from flask_restful import current_app


class RentConnector(ServiceConnector):
    """
    Class to connect with Rent service
    """

    def get_rent(self, user_id, rent_id):
        """
        Method to get rent from Rent service

        :param user_id:
        :param rent_id:
        :return: (response code, response data in json)
        """
        code, body = self.send_get_request('/user/{}/rent/{}'.
                                           format(user_id, rent_id))
        current_app.logger.debug("Response from rent: {}, {}".format(body, code))

        return code, body

    def get_rents_for_user(self, user_id):
        """
        Method to get all rents from Rent serive to user

        :param user_id:
        :return: (response code, response data in json)
        """

        code, body = self.send_get_request('/user/{}/rent'.format(user_id))
        current_app.logger.debug("Response from rent: {}, {}".format(body, code))

        return code, body

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

    def delete_rent(self, rent_id):
        """
        Method to delete rent in Rent service

        :param rent_id:
        :return: (response code, response data in json)
        """

        code, body = self.send_delete_request('/rent/{}'.format(rent_id))

        current_app.logger.debug("Response from rent: {}, {}".format(body, code))

        return code, {'message': 'rent was deleted'}
