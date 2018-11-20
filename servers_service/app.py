from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from .const import DB_URI
from servers_service.resources.server import Server


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % DB_URI
api = Api(app)
db = SQLAlchemy(app)


api.add_resource(Server, '/server',
                         '/server/<int:server_id>')