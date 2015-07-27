__author__ = 'Xu Zhao'

from app import db
from flask.ext.login import UserMixin
from . import login_manager

class Principal(UserMixin, db.Model):
    __tablename__ = "principal"
    # id is used for flask.login
    id = db.Column(db.Integer, primary_key=True)
    Email = db.Column(db.String(32), nullable=False)
    Password = db.Column(db.String(32), nullable=False)
    Name = db.Column(db.Unicode(64), nullable=False)
    Role = db.Column(db.String(1), nullable=False)
    Address = db.Column(db.Unicode(64))
    Contacts = db.Column(db.Unicode(16), nullable=False)
    Telephone = db.Column(db.String(16), nullable=False)
    RegTime = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return '%r' % self.Email

@login_manager.user_loader
def load_user(userid):
    return Principal.query.get(int(userid))
