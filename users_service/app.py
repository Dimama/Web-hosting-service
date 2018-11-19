from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/dimama/db/users.db'
api = Api(app)
db = SQLAlchemy(app)


@app.route('/')
def hello():
    return "USERS"