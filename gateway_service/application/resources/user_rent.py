from flask_restful import Resource, reqparse, current_app
from flask import request
from application.servers_connector import ServersConnector
from application.users_connector import UsersConnector
from application.rent_connector import RentConnector
from application.const import SERVERS_SERVICE_ADDRESS as serv_addr
from application.const import USERS_SERVICE_ADDRESS as users_addr
from application.const import RENT_SERVICE_ADDRESS as rent_addr


class UserRent(Resource):
    """
    Class to work with requests to urls like '/user/../rent/...'
    """

    def __init__(self):
        self.post_parser = reqparse.RequestParser()
        self.post_parser.add_argument('server_id', type=int, required=True,
                                      location='json', help="server id is not set")
        self.post_parser.add_argument('duration', type=int, required=True,
                                      location='json', help='duration is not set')

        super(UserRent, self).__init__()

    def get(self, user_id):

        current_app.logger.info('GET: {}'.format(request.full_path))

        s_conn = ServersConnector(serv_addr)
        r_conn = RentConnector(rent_addr)

        status, body = r_conn.get_rents_for_user(user_id)
        if status == 404:
            return body, status

        users_rents = []
        for rent in body['rents']:
            _, s_body = s_conn.get_server_by_id(rent['server_id'])
            resp_rent = s_body['server info']
            resp_rent.update(rent)
            resp_rent.pop('user_id')
            resp_rent.pop('server_id')
            resp_rent.pop('id')
            resp_rent.pop('count')
            users_rents.append(resp_rent)

        return {'user rents': users_rents}, 200

    def post(self, user_id):

        current_app.logger.info('POST: {} with body {}'.format(request.full_path,
                                                               request.get_json()))

        # 400 - bad request (validate body data)
        args = self.post_parser.parse_args()
        server_id = args['server_id']

        # check server available
        s_conn = ServersConnector(serv_addr)
        status, body = s_conn.get_server_available_count_and_price(server_id)
        if status == 404 or status == 422:  # server not found or no available
            return body, status

        price = body['price']
        duration = args['duration']

        # check user bills
        u_conn = UsersConnector(users_addr)
        status, body = u_conn.get_user_bill_money_count(user_id)
        if status == 404 or status == 422:  # user not found or no money on bill
            return body, status

        # compare price
        total_price = duration * price
        user_bill_money = body['money']

        if total_price > user_bill_money:  # not enough money on bill
            return {'message': 'not enough money on bill'}, 422

        # update user bill
        status, body = u_conn.decrease_user_bill(user_id, total_price)
        if status == 400:
            return body, status

        # decrease server_available
        status, body = s_conn.change_server_available(server_id, decrease=True)
        if status == 400 or status == 404:
            return body, status

        r_conn = RentConnector(rent_addr)
        status, body = r_conn.create_rent(user_id, server_id, duration)

        return body, status

    def delete(self, user_id, rent_id):

        current_app.logger.info('DELETE: {}'.format(request.full_path))
        r_conn = RentConnector(rent_addr)

        status, body = r_conn.get_rent(user_id, rent_id)
        if status == 404:
            return body, status

        server_id = body['server_id']
        s_conn = ServersConnector(serv_addr)
        _ = s_conn.change_server_available(server_id, decrease=False)

        status, body = r_conn.delete_rent(rent_id)

        return body, status
