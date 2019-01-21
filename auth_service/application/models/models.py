from application import db
from passlib.hash import pbkdf2_sha256 as sha256

class UserModel(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    @staticmethod
    def find_by_login(login):
        return UserModel.query.filter_by(login=login).first()

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)


class UserAppCode(db.Model):

    __tablename__ = 'codes'

    code = db.Column(db.Integer, primary_key=True)
    app_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)

    @staticmethod
    def find(user_id, app_id):
        return UserAppCode.query.filter_by(app_id=app_id, user_id=user_id).first()

    @staticmethod
    def find_by_code(code):
        return UserAppCode.query.filter_by(code=code).first()

    @staticmethod
    def update_code(user_id, app_id, code):
        record = UserAppCode.find(user_id, app_id)
        record.code = code
        db.session.commit()

    @staticmethod
    def create_code_record(code, app_id, user_id):
        db.session.add(UserAppCode(code=code, app_id=app_id, user_id=user_id))
        db.session.commit()
