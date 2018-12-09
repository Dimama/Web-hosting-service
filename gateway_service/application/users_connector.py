from .service_connector import ServiceConnector
from flask_restful import current_app


class UsersConnector(ServiceConnector):
    """
    Class to connect with Users Service
    """

    def get_user_bill_money_count(self, user_id):
        """
        Method to get count of money on user's bill

        :param user_id: id of user whose bill info need to get
        :return: (response code, response data in json)
        """

        url = '/user/{}'.format(user_id)

        code, body = self.send_get_request(url)

        current_app.logger.debug("Response from users: {}, {}".format(body, code))

        if code == 404:
            return code, body
        if body['user info']['money'] == 0:
            return 422, {'message': 'no money on bill'}

        return code, {'money': body['user info']['money']}

    def decrease_user_bill(self, user_id, price):
        """
        Method to decrease user bill

        :param user_id: id of user whose bill need to decrease
        :param price: rent amount that need to deducted from user bill
        :return: (response code, response data in json)
        """

        url = '/user/{}'.format(user_id)

        code, body = self.send_put_request(url, {'price': price})

        current_app.logger.debug("Response from users: {}, {}".format(body, code))

        if code == 404 or code == 400:
            return code, body

        return code, {'message': 'user bill updated'}