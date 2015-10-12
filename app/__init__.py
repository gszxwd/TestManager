__author__ = 'Xu Zhao'

# Factory Patton

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bootstrap import Bootstrap
from flask.ext.mail import Mail
from flask.ext.login import LoginManager
from config import config
import datetime

db = SQLAlchemy()
bootstrap = Bootstrap()
mail = Mail()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = '.login'

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    bootstrap.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

    # security setting
    app.secret_key="youdon'tknwhatIT1s"
    app.permanent_session_lifetime = datetime.timedelta(minutes=30)

    # register blueprint
    from .main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    return app
