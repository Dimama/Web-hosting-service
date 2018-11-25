from flask_script import Manager
from application import create_app
from application.setup_db import setup_servers_db, clear_servers_db

app = create_app()
manager = Manager(app)


@manager.command
def run():
    app.run(host='localhost', port=8082, debug=True)


@manager.command
def test():
    print("Tests here")


@manager.command
def setup_db():
    setup_servers_db()


@manager.command
def clear_db():
    clear_servers_db()


if __name__ == '__main__':
    manager.run()
