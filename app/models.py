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
        return '%r' % self.Name

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

class TestContract(db.Model):
    __tablename__ = "testcontract"
    ContractID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(64), nullable=False)
    Category = db.Column(db.String(1), nullable=False)
    Function = db.Column(db.String(128), nullable=False)
    Version = db.Column(db.String(16), nullable=False)
    OnlineTime = db.Column(db.DateTime, nullable=False)
    IsUpdated = db.Column(db.Boolean, nullable=False)
    Budgetary = db.Column(db.Float, nullable=False)
    RangeRate = db.Column(db.String(1), nullable=False)
    CapacityRate = db.Column(db.String(1), nullable=False)
    SafetyRate = db.Column(db.String(1), nullable=False)
    TestRank = db.Column(db.String(1), nullable=False)
    AdditionReq = db.Column(db.String(80))
    PMail = db.Column(db.String(32), nullable=False)
    TName = db.Column(db.String(32), nullable=False)
    RecordTime = db.Column(db.DateTime, nullable=False)

class TestEvidence(db.Model):
    __tablename__ = "testevidence"
    ID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(64), nullable=False)
    TMail = db.Column(db.String(32), nullable=False)
    TestStart = db.Column(db.DateTime, nullable=False)
    TestEnd = db.Column(db.DateTime, nullable=False)
    BasicReq = db.Column(db.String(80), nullable=False)
    AddtionReq = db.Column(db.String(80))
    TestEnv = db.Column(db.String(1), nullable=False)
    RegressNum = db.Column(db.Integer, nullable=False)
    Version = db.Column(db.String(16), nullable=False)
    CodeLines = db.Column(db.BigInteger, nullable=False)
    DesignCases = db.Column(db.Integer, nullable=False)
    PassedCases = db.Column(db.Integer, nullable=False)
    FFatalBugs = db.Column(db.Integer, nullable=False)
    RFatalBugs = db.Column(db.Integer, nullable=False)
    FCriticBugs = db.Column(db.Integer, nullable=False)
    RCriticBugs = db.Column(db.Integer, nullable=False)
    FCommBugs = db.Column(db.Integer, nullable=False)
    RCommBugs = db.Column(db.Integer, nullable=False)
    FAdviseBugs = db.Column(db.Integer, nullable=False)
    RAdviseBugs = db.Column(db.Integer, nullable=False)
    UpdateTime = db.Column(db.DateTime, nullable=False)
    EvalScore = db.Column(db.Numeric)

class Advice(db.Model):
    __tablename__ = "advice"
    ID = db.Column(db.Integer, primary_key=True)
    TName = db.Column(db.String(32), nullable=False)
    Content = db.Column(db.String(256), nullable=False)
    AdviceTime = db.Column(db.DateTime, nullable=False)

@login_manager.user_loader
def load_user(userid):
    return Principal.query.get(int(userid)) or Tester.query.get(int(userid))
