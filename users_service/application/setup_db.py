from application import db
from application.models.models import UserModel, UserBillsModel


def setup_users_db():
    db.create_all()

    db.session.add(UserModel(username='I. Ivanov', account_type='free'))
    db.session.add(UserModel(username='Melnikov Dmitry', account_type='premium'))
    db.session.add(UserModel(username='J. Bill', account_type='free'))

    db.session.commit()

    db.session.add(UserBillsModel(user_id=1, money_count=200))
    db.session.add(UserBillsModel(user_id=2, money_count=1000))
    db.session.add(UserBillsModel(user_id=3))

    db.session.commit()


def clear_users_db():
    engine = db.engine
    UserModel.__table__.drop(engine)
    UserBillsModel.__table__.drop(engine)
