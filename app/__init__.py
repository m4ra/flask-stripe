from flask import Flask
#from flask.ext.bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
#from flask.ext.login import LoginManager
from flask_seasurf import SeaSurf
#import logging
from config import config

db = SQLAlchemy()
csrf = SeaSurf()

def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

#    bootstrap.init_app(app)
    db.init_app(app)
    csrf.init_app(app)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')


    return app

