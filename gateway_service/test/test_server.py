from application import create_app
from unittest import TestCase


class TestServerResource(TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client

    def test_bad_url(self):
        res = self.client().get('/server')
        self.assertEqual(res.status_code, 400)

    def test_pagination(self):
        res = self.client().get('/server?page=1&size=1')
        self.assertEqual(res.status_code, 200)

