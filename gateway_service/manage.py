from flask_script import Manager
from application import create_app

app = create_app()
manager = Manager(app)


@manager.command
def run():
    app.run(host='localhost', port=8080, debug=True)


@manager.command
def test():
    print("Tests here")


if __name__ == '__main__':
    manager.run()
