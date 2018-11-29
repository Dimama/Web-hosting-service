from application import db


class RentModel(db.Model):

    __tablename__ = 'rents'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    server_id = db.Column(db.Integer, nullable=False)
    duration = db.Column(db.Integer, nullable=False)

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
