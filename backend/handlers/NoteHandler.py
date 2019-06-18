from backend.handlers import *
import os


def get_note(document_id, user_id):
    user = User.objects(id=str(user_id)).first()
    user_name = user.username
    doc = Documents.objects(id=str(document_id)).first()
    doc_name = doc.save_name
    note_flag = doc.save_note
    if not note_flag:
        os.mkdir('./' + 'md/' + user_name)
        # 新建笔记
        with open('./md/' + user_name + '/' + doc_name + '.md', 'a+') as f:
            f.close()
        doc.update(set__save_note=1)
        note = ''
        code = 200
    else:
        with open('./md/' + user_name + '/' + doc_name + '.md', 'rb') as f:
            note = f.read()
            f.close()
            code = 200
    return note, code
