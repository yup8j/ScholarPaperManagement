from backend.resources import *
from backend.handlers.NoteHandler import *


class GetNote(API):
    """
    获取笔记：没有则新建，有则取出
    """
    @jwt_required
    def post(self):
        user_id = get_jwt_identity()
        request.get_json(force=True)
        parse = reqparse.RequestParser()
        parse.add_argument('document_id', type=str)
        args = parse.parse_args()
        document_id = args['document_id']
        note, code = get_note(document_id=document_id, user_id=user_id)
        # note = note.replace('\n', '<br/>')
        self.response = make_response()
        self.response.status_code = code
        self.response = jsonify({"note": str(note)})
        return self.response


class SaveNote(API):
    """
    保存笔记
    """

    @jwt_required
    def post(self):
        user_id = get_jwt_identity()
        request.get_json(force=True)
        parse = reqparse.RequestParser()
        parse.add_argument('document_id', type=str)
        parse.add_argument('note_content', type=str)
        args = parse.parse_args()
        document_id = args['document_id']
        note_content = args['note_content']
        code = save_note(document_id=document_id, user_id=user_id, note_content=note_content)
        self.response = make_response()
        self.response.status_code = code
        return self.response
