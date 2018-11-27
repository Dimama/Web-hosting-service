from flask_script import Manager
from application import create_app
from application.setup_db import setup_users_db, clear_users_db

app = create_app()
manager = Manager(app)


@manager.command
def run():
    app.run(host='localhost', port=8081, debug=True)


@manager.command
def test():
    print("Tests here")


@manager.command
def setup_db():
    setup_users_db()


@manager.command
def clear_db():
    clear_users_db()

if __name__ == '__main__':
    manager.run()
