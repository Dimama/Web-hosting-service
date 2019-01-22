from application import db
from application.models.models import UserModel, UserAppCode


def setup_auth_db():
    db.create_all()

    db.session.add(UserModel(login="IIvanov",
                             password=UserModel.generate_hash('password')))
    db.session.add(UserModel(login="amamid",
                             password=UserModel.generate_hash('qwerty')))
    db.session.add(UserModel(login="john",
                             password=UserModel.generate_hash('password')))

    db.session.commit()


def clear_auth_db():
    engine = db.engine
    UserModel.__table__.drop(engine)
    UserAppCode.__table__.drop(engine)