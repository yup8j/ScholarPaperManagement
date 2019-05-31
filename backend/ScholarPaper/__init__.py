#-*-coding:utf-8 -*-
from .models.login import *
from flask import Flask
from werkzeug.utils import import_string
from .models import *
from .resources import *


def create_app():
    app = Flask(__name__)
    for bp_name in blueprints:
        bp = import_string(bp_name)
        app.register_blueprint(bp)
    return app