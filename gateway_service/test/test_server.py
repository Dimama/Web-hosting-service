from application import create_app
from unittest import TestCase
from unittest.mock import patch


class TestServerResource(TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client

    def test_bad_pagination(self):
        res = self.client().get('/server?page=1&size=6')
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json, {"message":
                                    {"size": "Incorrect size per page"}})

    @patch('application.servers_connector.ServersConnector.get_servers_with_pag')
    def test_pagination(self, mock):
        mock.return_value =\
            (200, {'servers': [{'id': 1,
                                'OS': 'CentOS7',
                                'RAM': 16,
                                'CPU': 6,
                                'Drive': 320}]})

        res = self.client().get('/server?page=1&size=1')

        self.assertEqual(res.status_code, 200)

    @patch('application.servers_connector.ServersConnector.get_server_by_id')
    def test_get_server_by_id(self, mock):
        mock.return_value =\
            (200, {'server info': [{'id': 1,
                                'OS': 'CentOS7',
                                'RAM': 16,
                                'CPU': 6,
                                'Drive': 320}]})

        res = self.client().get('/server/1')

        self.assertEqual(res.status_code, 200)
