#-*-coding:utf-8 -*-
from .required_modules import *
from ..models.login import *

db_config = {
    'db': User.objects
}

login = Blueprint('login', __name__)
api = Api(login)

api.add_resource(PreLoginAPI, '/login1', resource_class_kwargs=db_config)
api.add_resource(LoginAPI, '/login2', resource_class_kwargs=db_config)
