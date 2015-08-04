__author__ = 'Xu Zhao'

from app import db
from flask.ext.login import UserMixin
from . import login_manager

class Principal(UserMixin, db.Model):
    __tablename__ = "principal"
    # id is used for flask.login
    id = db.Column(db.Integer, primary_key=True)
    Email = db.Column(db.String(32), unique=True, nullable=False)
    Password = db.Column(db.String(32), nullable=False)
    Name = db.Column(db.Unicode(64), nullable=False)
    Role = db.Column(db.String(1), nullable=False)
    Address = db.Column(db.Unicode(64))
    Contacts = db.Column(db.Unicode(16), nullable=False)
    Telephone = db.Column(db.String(16), nullable=False)
    RegTime = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return '%r' % self.Email

class Tester(UserMixin, db.Model):
    __tablename__ = "tester"
    # id is used for flask.login
    id = db.Column(db.Integer, primary_key=True)
    Email = db.Column(db.String(32), unique=True, nullable=False)
    Password = db.Column(db.String(32), nullable=False)
    Name = db.Column(db.Unicode(64), nullable=False)
    Role = db.Column(db.String(1), nullable=False)
    Address = db.Column(db.Unicode(64))
    Contacts = db.Column(db.Unicode(16), nullable=False)
    Telephone = db.Column(db.String(16), nullable=False)
    RegTime = db.Column(db.DateTime, nullable=False)
    # new for Tester
    HasCMA = db.Column(db.Boolean, nullable=False)
    CMAStart = db.Column(db.DateTime)
    CMAEnd = db.Column(db.DateTime)
    CMAPath = db.Column(db.String(64))
    HasCNAS = db.Column(db.Boolean, nullable=False)
    CNASStart = db.Column(db.DateTime)
    CNASEnd = db.Column(db.DateTime)
    CNASPath = db.Column(db.String(64))
    HasCert = db.Column(db.Boolean, nullable=False)
    CertStart = db.Column(db.DateTime)
    CertEnd = db.Column(db.DateTime)
    CertPath = db.Column(db.String(64))
    TestRange = db.Column(db.String(64))
    EstbTime = db.Column(db.DateTime)
    RegTime = db.Column(db.DateTime, nullable=False)
    IsChecked = db.Column(db.Boolean, nullable=False)
    CheckName = db.Column(db.Unicode(64))
    CheckTime = db.Column(db.DateTime)

@login_manager.user_loader
def load_user(userid):
    return Principal.query.get(int(userid))
