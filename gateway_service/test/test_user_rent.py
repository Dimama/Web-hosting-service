from application import create_app
from unittest import TestCase
from unittest.mock import patch


class TestServerResource(TestCase):

    def setUp(self):

        self.app = create_app()
        self.client = self.app.test_client

    @patch('application.rent_connector.RentConnector.get_rents_for_user')
    def test_no_rents_for_user(self, rent_mock):

        rent_mock.return_value = (404, {'message': 'no rents for user'})
        res = self.client().get('/user/1/rent')
        self.assertEqual(res.status_code, 404)

    @patch('application.servers_connector.ServersConnector.get_server_by_id')
    @patch('application.rent_connector.RentConnector.get_rents_for_user')
    def test_rent_for_user(self, rent_mock, server_mock):

        rent_mock.return_value = (200, {'rents': [{'id': 3,
                                                   'user_id': 1,
                                                   'server_id': 1,
                                                   'duration': 10}]})
        server_mock.return_value = (200, {'server info':
                                                {'id': 1,
                                                'OS': 'CentOS7',
                                                'RAM': 16,
                                                'CPU': 6,
                                                'count': 10,
                                                'Drive': 320}})
        res = self.client().get('/user/1/rent')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json['user rents']), 1)

    @patch('application.rent_connector.RentConnector.get_rent')
    @patch('application.servers_connector.ServersConnector.change_server_available')
    @patch('application.rent_connector.RentConnector.delete_rent')
    def test_success_delete_rent(self, delete_mock, change_mock, get_mock):

        delete_mock.return_value = (204, {'message': 'rent deleted'})
        change_mock.return_value = (200, {'available count': 10})
        get_mock.return_value = (200, {'id': 1, 'user_id': 1,
                                       'server_id': 5, 'duration': 1})

        res = self.client().delete('/user/1/rent/1')
        self.assertEqual(res.status_code, 204)

    @patch('application.rent_connector.RentConnector.get_rent')
    def test_delete_not_existed_rent(self, get_mock):

        get_mock.return_value = (404, {'message': 'rent not found'})
        res = self.client().delete('/user/1/rent/10')
        self.assertEqual(res.status_code, 404)

    def test_bad_body_for_post(self):

        res = self.client().post('/user/1/rent', json={'server_id': 1})
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json, {'message': {'duration': 'duration is not set'}})

    @patch('application.servers_connector.ServersConnector.'
           'get_server_available_count_and_price')
    def test_no_available_servers(self, get_mock):

        get_mock.return_value = (422, {'message': 'no available servers'})

        res = self.client().post('/user/1/rent', json={'server_id': 1,
                                                       'duration': 3})
        self.assertEqual(res.status_code, 422)

    @patch('application.servers_connector.ServersConnector.'
           'get_server_available_count_and_price')
    @patch('application.users_connector.UsersConnector.get_user_bill_money_count')
    @patch('application.users_connector.UsersConnector.decrease_user_bill')
    @patch('application.servers_connector.ServersConnector.change_server_available')
    @patch('application.rent_connector.RentConnector.create_rent')
    def test_success_create_rent(self, create_mock, change_mock, decrease_mock,
                                 get_money_mock, get_count_mock):

        create_mock.return_value = (201, {'id': 1, 'user_id': 1,
                                          'server_id': 1, 'duration': 1})
        change_mock.return_value = (200, {'available count': 9})
        decrease_mock.return_value = (200, {'bill': 1040})
        get_money_mock.return_value = (200, {'id': 1, 'name': 'ivan',
                                             'acc_type': 'free', 'money': 2000})
        get_count_mock.return_value = (200, {'count': 10, 'price': 960})

        res = self.client().post('/user/1/rent', json={'server_id': 1,
                                                       'duration': 1})
        self.assertEqual(res.status_code, 201)

    @patch('application.servers_connector.ServersConnector.'
           'get_server_available_count_and_price')
    @patch('application.users_connector.UsersConnector.get_user_bill_money_count')
    def test_no_such_money(self, get_money_mock, get_count_mock):

        get_money_mock.return_value = (200, {'id': 1, 'name': 'ivan',
                                             'acc_type': 'free', 'money': 2000})
        get_count_mock.return_value = (200, {'count': 10, 'price': 960})

        res = self.client().post('/user/1/rent', json={'server_id': 1,
                                                       'duration': 3})

        self.assertEqual(res.status_code, 422)
        self.assertEqual(res.json, {'message': 'not enough money on bill'})