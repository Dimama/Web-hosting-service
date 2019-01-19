from flask_restful import Resource, reqparse
from application.models.models import RentModel
from flask import current_app, request
from application.exceptions import NoRentException
from flask_jwt_extended import jwt_required


class Rent(Resource):

    def __init__(self):
        self.post_reqparser = reqparse.RequestParser()
        self.post_reqparser.add_argument('user_id', type=int, required=True,
                                         location='json', help="user_id is not set")
        self.post_reqparser.add_argument('server_id', type=int, required=True,
                                         location='json', help="server__id is not set")
        self.post_reqparser.add_argument('duration', type=int, required=True,
                                         location='json', help="duration is not set")

    #@jwt_required
    def post(self):
        """
        Method to process Post request to Rent service

        :return: (response data in json, response status code)
        """
        current_app.logger.info('POST: {}  {}'.format(request.full_path,
                                                     request.get_json(force=True)))
        args = self.post_reqparser.parse_args()

        uid, sid, dur = args['user_id'], args['server_id'], args['duration']

        # TODO: may be try..except
        rent_id = RentModel.create_rent(uid, sid, dur)

        return {'message': 'rent with id: {} created'.format(rent_id)}, 201

    #@jwt_required
    def get(self, user_id, rent_id=None):
        """
        Method to process get responses for rent resources

        :param user_id:
        :param rent_id:
        :return: (response data in json, response status code)
        """

        current_app.logger.info('GET: {}'.format(request.full_path))

        if rent_id is None:
            objects = RentModel.get_rents_for_user(user_id)

            if not objects:
                current_app.logger.warn("Resource not found")
                return {'message': 'rents not found'}, 404
            else:
                return {'rents': [o.to_json() for o in objects]}, 200

        else:
            rent = RentModel.get_rent_for_user_by_id(user_id, rent_id)
            if rent is None:
                current_app.logger.warn("Resource not found")
                return {'message': 'rent not found'}, 404
            else:
                return rent.to_json(), 200

    #@jwt_required
    def delete(self, rent_id):
        """
        Method to process DELETE request to Rent service

        :param rent_id: id of record which need to delete
        :return: (response data in json, response status code)
        """

        current_app.logger.info('DELETE: {}'.format(request.full_path))

        try:
            RentModel.delete_rent(rent_id)
        except NoRentException as e:
            current_app.logger.warn(str(e))
            return {'message': str(e)}, 404
        else:
            return {'message': 'rent with id: {} deleted'.format(rent_id)}, 204
