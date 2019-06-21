from backend.resources import *
from backend.handlers.ColorHandler import *


class ColorChange(API):
    @jwt_required
    def post(self):
        user_id = get_jwt_identity()
        request.get_json(force=True)
        parse = reqparse.RequestParser()
        parse.add_argument('document_id', type=str)
        parse.add_argument('mark_type', type=int)
        args = parse.parse_args()
        document_id = args['document_id']
        color_type = args['mark_type']
        self.response = make_response()
        self.response.code = change_color(user_id=user_id, document_id=document_id, mark_type=color_type)
        return self.response
