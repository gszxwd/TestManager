# -*- coding: utf-8 -*-
__author__ = 'Xu Zhao'

import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
from app.models import Principal

email = u"auditor@163.com"
password = u"auditor"
name = u"交通运输部科技司"
address = u"交通运输部"
contacts = u"小红"
telephone = u"82337654"
regtime = datetime.now()

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data-dev.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)
db.init_app(app)
db.create_all()
prcp = Principal(Email=email,
                 Password=password,
                 Name=name,
                 Role="5",
                 Address=address,
                 Contacts=contacts,
                 Telephone=telephone,
                 RegTime=regtime)
db.session.add(prcp)
db.session.commit()
print u"管理员"+contacts+u"添加成功！"