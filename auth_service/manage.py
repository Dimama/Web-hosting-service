from flask_script import Manager
from application import create_app
from application.setup_db import setup_auth_db, clear_auth_db

app = create_app()
manager = Manager(app)


@manager.command
def run():
    app.run(host='localhost', port=8084, debug=True)


@manager.command
def setup_db():
    setup_auth_db()


@manager.command
def clear_db():
    clear_auth_db()


if __name__ == '__main__':
    manager.run()
