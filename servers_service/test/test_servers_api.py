from application import create_app
from unittest import TestCase
from unittest.mock import patch
from application.models.models import ServerModel, ServerInfoModel


class TestUsersService(TestCase):

    def setUp(self):

        self.app = create_app(testing_mode=True)
        self.client = self.app.test_client

    def test_bad_request(self):

        res = self.client().get('/server?page=1&size=7')
        self.assertEqual(res.status_code, 400)

    @patch('application.models.models.ServerModel.get_servers_with_pagination')
    def test_no_servers(self, get_mock):

        get_mock.return_value = None
        res = self.client().get('/server?page=3')

        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.json, {'message': 'servers not found'})

    @patch('application.models.models.ServerModel.get_servers_with_pagination')
    def test_get_to_servers(self, get_mock):

        objects = [ServerModel(id=1, os='Ubuntu 16.04 Server', ram=16, cpu=6, drive_size=320),
                   ServerModel(id=2, os='Ubuntu 18.04 Server', ram=192, cpu=32, drive_size=3840)]

        get_mock.return_value = objects

        res = self.client().get('/server?page=1&size=2')

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json, {'servers': [
                                    {'CPU': 6, 'Drive': 320,
                                     'OS': 'Ubuntu 16.04 Server',
                                     'RAM': 16, 'id': 1},
                                    {'CPU': 32, 'Drive': 3840,
                                     'OS': 'Ubuntu 18.04 Server',
                                     'RAM': 192, 'id': 2}]})

    @patch('application.models.models.ServerModel.get_full_server_info_by_id')
    def test_server_not_found(self, get_mock):

        get_mock.return_value = None
        res = self.client().get('/server/15')

        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.json, {'message': 'server not found'})

    @patch('application.models.models.ServerModel.get_full_server_info_by_id')
    def test_get_full_info(self, get_mock):

        get_mock.return_value = (ServerModel(id=1, os='Ubuntu 16.04 Server',
                                             ram=16, cpu=6, drive_size=320),
                                 ServerInfoModel(id=1, price=80, count=20))
        res = self.client().get('/server/1')

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json, {'server info':
                                    {'CPU': 6, 'Drive': 320,
                                     'OS': 'Ubuntu 16.04 Server',
                                     'RAM': 16, 'count': 20,
                                     'id': 1, 'price': 80}})

    def test_update_count_bad_request(self):

        res = self.client().put('/server/1', json={'delta': '2'})
        self.assertEqual(res.status_code, 400)

    @patch('application.models.models.ServerInfoModel.update_server_available')
    def test_update_count(self, update_mock):

        update_mock.return_value = 3
        res = self.client().put('/server/1', json={'delta': '1'})

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json, {'available count': 3})

