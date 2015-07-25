__author__ = 'Xu Zhao'

from app import db

class Principal(db.Model):
    __tablename__ = "principal"
    Email = db.Column(db.String(32), primary_key=True, nullable=False)
    Password = db.Column(db.String(32), nullable=False)
    Name = db.Column(db.Unicode(64), nullable=False)
    Role = db.Column(db.String(1), nullable=False)
    Address = db.Column(db.Unicode(64))
    Contacts = db.Column(db.Unicode(16), nullable=False)
    Telephone = db.Column(db.String(16), nullable=False)
    RegTime = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return '%r' % self.Email