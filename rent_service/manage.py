from flask_script import Manager
from application import create_app
#from application.setup_db import setup_rent_db, clear_rent_db

app = create_app()
manager = Manager(app)


@manager.command
def run():
    app.run(host='localhost', port=8083, debug=True)


@manager.command
def test():
    print("Tests here")


@manager.command
def setup_db():
    pass
    # TODO: setup rent db
    #setup_rent_db()


@manager.command
def clear_db():
    pass
    # TODO: clear rent db
    #clear_rent_db()


if __name__ == '__main__':
    manager.run()
