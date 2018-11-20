from .app import db

class ServerConfiguration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    os = db.Column(db.String(40), nullable=False)
    ram = db.Column(db.Integer, default=16)
    cpu = db.Column(db.Integer, default=4)
    drive_size = db.Column(db.Integer, default=1000)

    def __repr__(self):
        return '<{} Server configuration: {} {} Gb {} cpu {} Gb>'.format(self.id,
                                                                         self.os,
                                                                         self.ram,
                                                                         self.cpu,
                                                                         self.drive_size)


class ConfigurationInfo(db.Model):
    id = db.Column(db.Integer,  db.ForeignKey('server_configuration.id'),
                   primary_key=True)
    price = db.Column(db.Float, nullable=False)
    count = db.Column(db.Integer, default=10)