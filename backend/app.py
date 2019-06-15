from flask import Blueprint
from flask_restful import Api
from backend.resources.login import *
from backend.resources.oss_control import *

api_bp = Blueprint('api', __name__)
api = Api(api_bp)
api.add_resource(PreLoginAPI, '/login1')
api.add_resource(LoginAPI, '/login2')
api.add_resource(UploadDocuments, '/upload')
