from application import create_app
from unittest import TestCase
from unittest.mock import patch
from test.mock_classes import FakeUser, FakeUserInfo


class TestUsersService(TestCase):

    def setUp(self):

        self.app = create_app(testing_mode=True)
        self.client = self.app.test_client

    @patch('application.models.models.UserModel.get_user_info_by_id')
    def test_no_user(self, user_mock):

        user_mock.return_value = None
        res = self.client().get('/user/1')
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.json, {'message': 'user not found'})

    @patch('application.models.models.UserModel.get_user_info_by_id')
    def test_get_existed_user(self, user_mock):

        user = FakeUser()
        user_info = FakeUserInfo()

        user_mock.return_value = (user, user_info)
        res = self.client().get('/user/1')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json, {'user info': {'acc_type': 'free',
                                                  'id': 1,
                                                  'money': 200,
                                                  'name': 'Ivan'}})

    def test_update_bill_with_bad_body(self):

        res = self.client().put('/user/1', json={'pprice': 50})
        self.assertEqual(res.status_code, 400)

    @patch('application.models.models.UserBillsModel.decrease_user_bill')
    def test_update_bill(self, bill_mock):

        bill_mock.return_value = 150
        res = self.client().put('/user/1', json={'price': 50})

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json, {'bill': 150})
