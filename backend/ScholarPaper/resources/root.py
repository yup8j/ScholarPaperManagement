#-*-coding:utf-8 -*-
from .required_modules import *
from ..models.root import *

db_config = {
    'db': User.objects
}

root = Blueprint('root', __name__)
api = Api(root)

api.add_resource(Main, '/', resource_class_kwargs=db_config)