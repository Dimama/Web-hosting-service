from application import db
from application.exceptions import NoRentException


class RentModel(db.Model):

    __tablename__ = 'rents'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    server_id = db.Column(db.Integer, nullable=False)
    duration = db.Column(db.Integer, nullable=False)

    def to_json(self):
        return {'id': self.id,
                'user_id': self.user_id,
                'server_id': self.server_id,
                'duration': self.duration}

    @staticmethod
    def get_rents_for_user(user_id):
        return RentModel.query.filter_by(user_id=user_id).all()

    @staticmethod
    def get_rent_for_user_by_id(user_id, rent_id):
        return RentModel.query.filter_by(user_id=user_id).\
            filter_by(id=rent_id).first()

    @staticmethod
    def create_rent(user_id, server_id, duration):
        """
        Method to create rent record in table 'rents'

        :param user_id:
        :param server_id:
        :param duration:
        :return: id of created rent
        """

        r_m = RentModel(user_id=user_id, server_id=server_id, duration=duration)

        db.session.add(r_m)
        db.session.commit()

        db.session.refresh(r_m)

        return r_m.id

    @staticmethod
    def delete_rent(rent_id):
        """
        Method to delete rent recor from table 'rents'

        :param rent_id:
        :return:
        """

        rent_obj = RentModel.query.filter_by(id=rent_id).first()
        if rent_obj is None:
            raise NoRentException('Rent with id: {} not found'.format(rent_id))
        else:
            db.session.delete(rent_obj)
            db.session.commit()




