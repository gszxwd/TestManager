__author__ = 'Xu Zhao'

from flask import Flask
from flask.ext.mail import Mail, Message

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.163.com'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'testermanager@163.com'
app.config['MAIL_PASSWORD'] = 'fdsmfxjpjzryhobx'

mail = Mail(app)
msg = Message('Notification', recipients=['gszxwd@163.com'],
              sender='testermanager@163.com')
msg.body = 'Please notify your department to attend the conference.'
#msg.html = '<b>Please </b>'

with app.app_context():
    mail.send(msg)
    print 'send ok'
