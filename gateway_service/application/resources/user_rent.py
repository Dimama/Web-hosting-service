from flask_restful import Resource, reqparse, current_app
from flask import jsonify, request
from application.servers_connector import ServersConnector
from application.users_connector import UsersConnector
from application.const import SERVERS_SERVICE_ADDRESS as serv_addr
from application.const import USERS_SERVICE_ADDRESS as users_addr


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
        # add pagination
        # 400 - bad request
        # 200 - ok
        # 404 - not found
        # get configurations for user
        # get configurations from servers_service
        # accumulate data

        return jsonify({"id": user_id, "method": "get"})

    def post(self, user_id):

        current_app.logger.info('POST: {} with body {}'.format(request.full_path, request.get_json()))

        # 400 - bad request (validate body data) +
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
        user_bill_money = body['money_count']

        if total_price > user_bill_money:  # not enough money on bill
            return 422, {'message': 'not enough money on bill'}

        # update user bill
        # update server_available
        # create rent record and sent record to user (200)

        return jsonify({"id": user_id, "method": "post"})

    def delete(self, user_id, rent_id):
        # 400 - bad request
        # delete rent (404 not found rent)
        # update server available
        # return 204
        return jsonify({"user_id": user_id, "rent_id": rent_id,
                        "method": "delete"})