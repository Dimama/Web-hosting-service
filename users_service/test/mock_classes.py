class FakeUser(object):
    def to_json(self):
        return {'id': 1,
                'name': 'Ivan',
                'acc_type': 'free'}


class FakeUserInfo(object):
    def to_json(self):
        return {'money': 200}