from flask import Blueprint
from flask_restful import Api
from backend.resources.login import *
from backend.resources.oss_control import *
from backend.resources.notes import *

api_bp = Blueprint('api', __name__)
api = Api(api_bp)
api.add_resource(PreLoginAPI, '/login1')
api.add_resource(LoginAPI, '/login2')
api.add_resource(UploadDocuments, '/upload')
api.add_resource(DownloadDocuments, '/getdoc/<document_id>')
api.add_resource(DeleteDocuments, '/removedoc')
api.add_resource(GetNote, '/getnote')
api.add_resource(SaveNote, '/savenote')
