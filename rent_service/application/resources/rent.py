from flask_restful import Resource, reqparse
from application.models.models import RentModel
from flask import current_app, request


class Rent(Resource):

    def __init__(self):
        self.post_reqparser = reqparse.RequestParser()
        self.post_reqparser.add_argument('user_id', type=int, required=True,
                                         location='json', help="user_id is not set")
        self.post_reqparser.add_argument('server_id', type=int, required=True,
                                         location='json', help="server__id is not set")
        self.post_reqparser.add_argument('duration', type=int, required=True,
                                         location='json', help="duration is not set")

    def post(self):
        """
        Method to process Post request to Rent service

        :return: (response data in json, response status code)
        """
        print(request.form.to_dict())
        current_app.logger.info('POST: {}  {}'.format(request.full_path,
                                                     request.get_json(force=True)))
        args = self.post_reqparser.parse_args()

        uid, sid, dur = args['user_id'], args['server_id'], args['duration']

        # TODO: may be try..except
        rent_id = RentModel.create_rent(uid, sid, dur)

        return {'message': 'rent with id: {} created'.format(rent_id)}, 201

    def get(self):
        pass

    def delete(self):
        pass
