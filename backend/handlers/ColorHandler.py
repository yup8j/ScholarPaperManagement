from backend.handlers import *
from backend.models.db_models import Documents


def change_color(user_id, document_id, mark_type):
    try:
        Documents.objects(id=document_id).update(set__color=int(mark_type))
        code = 200
    except Exception as e:
        print(e)
        code = 403
    return code
