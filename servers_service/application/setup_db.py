from application import db
from application.models.models import ServerInfoModel, ServerModel


def setup_servers_db():
    db.create_all()

    db.session.add(ServerModel(os='CentOS7'))
    db.session.add(ServerModel(os='CentOS7', ram=32, cpu=8, drive_size=640))
    db.session.add(ServerModel(os='CentOS6', ram=2, cpu=2, drive_size=60))
    db.session.add(ServerModel(os='Ubuntu 16.04 Server', ram=16, cpu=6, drive_size=320))
    db.session.add(ServerModel(os='Ubuntu 18.04 Server', ram=192, cpu=32, drive_size=3840))
    db.session.add(ServerModel(os='Fedora 29', ram=48, cpu=12, drive_size=960))

    db.session.commit()

    db.session.add(ServerInfoModel(id=1, price=80, count=20))
    db.session.add(ServerInfoModel(id=2, price=160, count=30))
    db.session.add(ServerInfoModel(id=3, price=15, count=50))
    db.session.add(ServerInfoModel(id=4, price=80, count=10))
    db.session.add(ServerInfoModel(id=5, price=960, count=1))
    db.session.add(ServerInfoModel(id=6, price=240, count=10))

    db.session.commit()


def clear_servers_db():
    engine = db.engine
    ServerModel.__table__.drop(engine)
    ServerInfoModel.__table__.drop(engine)
