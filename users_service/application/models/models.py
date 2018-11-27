from application import db
from enum import Enum


class AccoutTypeEnum(Enum):
    free = 1
    premium = 2


class UserModel(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    account_type = db.Column(db.Enum(AccoutTypeEnum), default=AccoutTypeEnum.free)

    def to_json(self):
        pass

    @staticmethod
    def get_user_info_by_id(user_id):
        """
        Method to get user info (id, name, account type, money) using join

        :param user_id:
        :return (UserModel, UserBillsModel)
        """

        info = db.session.query(UserModel, UserBillsModel).\
            join(UserBillsModel).\
            filter(UserBillsModel.user_id == user_id)
        return info.first()

    def __repr__(self):
        return '<User: {} with id: {}>'.format(self.username, self.id)


class UserBillsModel(db.Model):

    __tablename__ = 'users_bills'

    def to_json(self):
        pass

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    money_count = db.Column(db.Float, default=0.0)
