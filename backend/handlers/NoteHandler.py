from backend.handlers import *
import os


def get_note(document_id, user_id):
    try:
        user = User.objects(id=str(user_id)).first()
        user_name = user.username
        doc = Documents.objects(id=str(document_id)).first()
        doc_name = doc.save_name
        note_flag = doc.save_note
    except Exception:
        return '', 403
    if not note_flag:
        path = './md/' + user_name + '/'
        if not os.path.isdir(path):
            os.makedirs(path)
        # 新建笔记
        try:
            with open('./md/' + user_name + '/' + doc_name + '.md', 'a+') as f:
                f.close()
            doc.update(set__save_note=1)
            note = ''
            code = 200
        except Exception:
            code = 403
            note = ''
    else:
        try:
            with open('./md/' + user_name + '/' + doc_name + '.md', 'r+') as f:
                note = f.read()
                f.close()
                code = 200
        except Exception:
            code = 403
            note = ''
    return note, code


def save_note(document_id, user_id, note_content):
    try:
        user = User.objects(id=str(user_id)).first()
        user_name = user.username
        doc = Documents.objects(id=str(document_id)).first()
        doc_name = doc.save_name
    except Exception:
        return 403
    path = './' + 'md/' + user_name
    try:
        with open('./md/' + user_name + '/' + doc_name + '.md', 'w') as f:
            f.write(note_content)
            f.close()
        code = 200
        return code
    except Exception as e:
        return 403
