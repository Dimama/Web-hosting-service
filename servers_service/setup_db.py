#run python -m servers_service.setup_db setup(clear)
from .models import db, ServerConfiguration, ConfigurationInfo
import sys


def setup_servers_db():
    db.create_all()

    db.session.add(ServerConfiguration(os='CentOS7'))
    db.session.add(ServerConfiguration(os='CentOS7', ram=32, cpu=8, drive_size=2000))
    db.session.add(ServerConfiguration(os='CentOS6', ram=16, cpu=4, drive_size=512))
    db.session.add(ServerConfiguration(os='Ubuntu 16.04 Server', ram=16, cpu=8, drive_size=1000))
    db.session.add(ServerConfiguration(os='Ubuntu 18.04 Server', ram=64, cpu=16, drive_size=4000))

    db.session.commit()

    db.session.add(ConfigurationInfo(id=1, price=20.5, count=500))
    db.session.add(ConfigurationInfo(id=2, price=50, count=120))
    db.session.add(ConfigurationInfo(id=3, price=10, count=50))
    db.session.add(ConfigurationInfo(id=4, price=75, count=200))
    db.session.add(ConfigurationInfo(id=5, price=90.5, count=100))

    db.session.commit()


def clear_servers_db():
    engine = db.engine
    ServerConfiguration.__table__.drop(engine)
    ConfigurationInfo.__table__.drop(engine)

if __name__ == '__main__':
    if sys.argv[1] == "clear":
        clear_servers_db()
    elif sys.argv[1] == "setup":
        setup_servers_db()
    else:
        print("Set option: clear/setup to drop/create tables in servers database")