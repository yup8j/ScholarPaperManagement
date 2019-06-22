from flask import Blueprint
from flask_restful import Api
from backend.resources.login import *
from backend.resources.oss_control import *
from backend.resources.notes import *
from backend.resources.info import *
from backend.resources.lib import *
from backend.resources.color import *

api_bp = Blueprint('api', __name__)
api = Api(api_bp)
api.add_resource(PreLoginAPI, '/login1')
api.add_resource(LoginAPI, '/login2')
api.add_resource(RegisterAPI, '/register')
api.add_resource(LogoutAPI, '/logout')
api.add_resource(UploadDocuments, '/upload')
api.add_resource(DownloadDocuments, '/getdoc/<document_id>')
api.add_resource(DeleteDocuments, '/removedoc')
api.add_resource(GetNote, '/getnote')
api.add_resource(SaveNote, '/savenote')
api.add_resource(GetInfo, '/getinfo')
api.add_resource(EditInfo, '/editinfo')
api.add_resource(AddLib, '/addlib')
api.add_resource(DeleteLib, '/deletelib')
api.add_resource(GetLib, '/getlib')
api.add_resource(ColorChange, '/mark')
api.add_resource(GetDocsInLib, '/getdocsinlib/<lib_type>')
api.add_resource(AddToLib, '/addtolib')
api.add_resource(RemoveFromLib, '/removefromlib')
api.add_resource(AddReadLater, '/addreadlater')
api.add_resource(RemoveFromReadLater, '/removefromreadlater')
api.add_resource(GetReadLater, '/getreadlater')
api.add_resource(UpgradeUser, '/upgrade')
