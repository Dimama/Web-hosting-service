from .app import db
from enum import Enum

class AccoutTypeEnum(Enum):
    free = 1
    premium = 2

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    account_type = db.Column(db.Enum(AccoutTypeEnum), default=AccoutTypeEnum.free)

    def __repr__(self):
        return '<User: {} with id: {}>'.format(self.username, self.id)

class UserBills(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    money_count = db.Column(db.Float, default=0.0)
