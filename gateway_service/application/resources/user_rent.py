from flask_restful import Resource, reqparse, current_app
from flask import request
from application.servers_connector import ServersConnector
from application.users_connector import UsersConnector
from application.rent_connector import RentConnector
from application.auth_connector import AuthConnector
from application.const import SERVERS_SERVICE_ADDRESS as serv_addr
from application.const import USERS_SERVICE_ADDRESS as users_addr
from application.const import RENT_SERVICE_ADDRESS as rent_addr
from application.const import AUTH_SERVICE_ADDRESS as auth_addr


def token_required(func):
    def _check_token(*args, **kwargs):
        auth_headers = request.headers.get('Authorization', '').split()

        if len(auth_headers) != 2:
            return {'message': 'Authorization header required.'}, 401
        if 'Bearer' not in auth_headers:
            return {'message': 'Authorization header format: Bearer `JWT`'}, 401

        a_conn = AuthConnector(auth_addr)

        status, body = a_conn.check_token(auth_headers[1])

        if status == 401:
            return body, status

        return func(*args, **kwargs)
    return _check_token


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

    @token_required
    def get(self, user_id):

        current_app.logger.info('GET: {}'.format(request.full_path))

        s_conn = ServersConnector(serv_addr, 'SERVERS')
        r_conn = RentConnector(rent_addr, 'RENT')

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
            resp_rent.pop('count')
            users_rents.append(resp_rent)

        return {'user rents': users_rents}, 200

    @token_required
    def post(self, user_id):

        current_app.logger.info('POST: {} with body {}'.format(request.full_path,
                                                               request.get_json()))

        # 400 - bad request (validate body data)
        args = self.post_parser.parse_args()
        server_id = args['server_id']

        # check server available
        s_conn = ServersConnector(serv_addr, 'SERVERS')
        status, body = s_conn.get_server_available_count_and_price(server_id)
        if status == 404 or status == 422:  # server not found or no available
            return body, status

        price = body['price']
        duration = args['duration']

        # check user bills
        u_conn = UsersConnector(users_addr, 'USERS')
        status, body = u_conn.get_user_bill_money_count(user_id)
        if status == 404 or status == 422:  # user not found or no money on bill
            return body, status

        # compare price
        total_price = duration * price
        user_bill_money = body['money']

        if total_price > user_bill_money:  # not enough money on bill
            return {'message': 'not enough money on bill'}, 422

        # update user bill
        status, body = u_conn.change_user_bill(user_id, total_price, decrease=True)
        if status == 400:
            return body, status

        # decrease server_available
        status, body = s_conn.change_server_available(server_id, decrease=True)
        if status == 400 or status == 404:
            return body, status

        r_conn = RentConnector(rent_addr, 'RENT')
        status, body = r_conn.create_rent(user_id, server_id, duration)

        # make rollback
        if status == 503:
            _ = s_conn.change_server_available(server_id, decrease=False)
            _ = u_conn.change_user_bill(user_id, total_price, decrease=False)
            return {'message': 'Can not create rent'}, 500

        return body, status

    @token_required
    def delete(self, user_id, rent_id):

        current_app.logger.info('DELETE: {}'.format(request.full_path))
        r_conn = RentConnector(rent_addr, 'RENT')

        status, body = r_conn.get_rent(user_id, rent_id)
        if status == 404:
            return body, status

        server_id = body['server_id']
        s_conn = ServersConnector(serv_addr, 'SERVERS')
        _ = s_conn.change_server_available(server_id, decrease=False)

        status, body = r_conn.delete_rent(rent_id)

        return body, status
