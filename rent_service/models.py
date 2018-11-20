from .app import db


class Rent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    server_id = db.Column(db.Integer, nullable=False)
    duration = db.Column(db.Integer, nullable=False)