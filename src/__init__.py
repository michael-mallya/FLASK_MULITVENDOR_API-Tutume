from flask import Flask

from .connect_ext import connect_ext
from .connect_api import connect_blueprint
from .extension import  mail


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('settings.py')
    connect_ext(app)
    connect_blueprint(app)
    mail.init_app(app)
    
    
    return app
