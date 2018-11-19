from flask import Flask
from flask_restful import Api
from gateway_service.resources.user_rent import UserRent
from gateway_service.resources.server import Server


app = Flask(__name__)
api = Api(app)

api.add_resource(Server, '/server',
                         '/server/<int:server_id>')
api.add_resource(UserRent, '/user/<int:user_id>/rent',
                           '/user/<int:user_id>/rent/<int:rent_id>')


