from application import db
import json

class ServerModel(db.Model):
    """
    Server Model
    """

    __tablename__ = 'servers'

    id = db.Column(db.Integer, primary_key=True)
    os = db.Column(db.String(40), nullable=False)
    ram = db.Column(db.Integer, default=16)
    cpu = db.Column(db.Integer, default=4)
    drive_size = db.Column(db.Integer, default=1000)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def to_json(self):
        return {'id': self.id,
                'OS': self.os,
                'RAM': self.ram,
                'CPU': self.cpu,
                'Drive': self.drive_size}

    @staticmethod
    def get_all_servers():
        return ServerModel.query.all()

    @staticmethod
    def get_server_by_id(server_id):
        return ServerModel.query.get(server_id)

    @staticmethod
    def get_servers_with_pagination(page, per_page):
        return ServerModel.query.paginate(page, per_page, False).items

    def __repr__(self):
        return '<{} Server configuration: {} {} Gb {} cpu {} Gb>'.format(self.id,
                                                                         self.os,
                                                                         self.ram,
                                                                         self.cpu,
                                                                         self.drive_size)


class ServerInfoModel(db.Model):
    """
    Additional Server info model
    """

    __tablename__ = 'servers_info'
    id = db.Column(db.Integer,  db.ForeignKey('servers.id'),
                   primary_key=True)
    price = db.Column(db.Float, nullable=False)
    count = db.Column(db.Integer, default=10)