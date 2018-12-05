from application import create_app
from unittest import TestCase
from unittest.mock import patch
from application.models.models import RentModel

class TestRentService(TestCase):

    def setUp(self):

        self.app = create_app(testing_mode=True)
        self.client = self.app.test_client

    def test_bad_post_request(self):

        res = self.client().post('/rent', json={'server_id': 1, 'duration': 2})
        self.assertEqual(res.status_code, 400)

    @patch('application.models.models.RentModel.create_rent')
    def test_create_rent(self, create_mock):

        create_mock.return_value = 1

        res = self.client().post('/rent', json={'user_id': 1, 'server_id': 1, 'duration': 2})
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.json, {'message': 'rent with id: 1 created'})

    @patch('application.models.models.RentModel.delete_rent')
    def test_delete_rent(self, delete_mock):

        res = self.client().delete('/rent/1')
        self.assertEqual(res.status_code, 204)

    @patch('application.models.models.RentModel.get_rents_for_user')
    def test_no_rents(self, get_mock):

        get_mock.return_value = None
        res = self.client().get('/user/1/rent')

        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.json, {'message': 'rents not found'})

    @patch('application.models.models.RentModel.get_rent_for_user_by_id')
    def test_no_rent(self, get_mock):

        get_mock.return_value = None
        res = self.client().get('/user/1/rent/2')

        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.json, {'message': 'rent not found'})

    @patch('application.models.models.RentModel.get_rents_for_user')
    def test_get_2_rents(self, get_mock):

        get_mock.return_value = [RentModel(id=1, user_id=1, server_id=1, duration=2),
                                 RentModel(id=2, user_id=1, server_id=5, duration=10)]
        res = self.client().get('/user/1/rent')

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json, {'rents': [
                                    {'duration': 2, 'id': 1,
                                     'server_id': 1, 'user_id': 1},
                                    {'duration': 10, 'id': 2,
                                     'server_id': 5, 'user_id': 1}]})

    @patch('application.models.models.RentModel.get_rent_for_user_by_id')
    def test_get_rent_by_id(self, get_mock):

        get_mock.return_value = RentModel(id=1, user_id=1, server_id=1, duration=2)
        res = self.client().get('/user/1/rent/1')

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json, {'duration': 2, 'id': 1,
                                    'server_id': 1, 'user_id': 1})