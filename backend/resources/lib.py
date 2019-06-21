from backend.resources import *
from backend.handlers.LibHandler import *
from flask_jwt_extended import jwt_required, get_jwt_identity


class AddLib(API):
    @jwt_required
    def post(self):
        """
        添加分类
        :return:
        """
        user_id = get_jwt_identity()
        self.response = make_response()
        request.get_json(force=True)
        parse = reqparse.RequestParser()
        parse.add_argument('lib_name', type=str)
        args = parse.parse_args()
        lib_name = args['lib_name']
        new_lib_id, code = add_lib(user_id=user_id, lib_name=lib_name)
        self.response.code = code
        return self.response
