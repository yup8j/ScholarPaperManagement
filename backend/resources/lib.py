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


class DeleteLib(API):
    @jwt_required
    def post(self):
        """
        删除分类
        :return:
        """
        user_id = get_jwt_identity()
        self.response = make_response()
        request.get_json(force=True)
        parse = reqparse.RequestParser()
        parse.add_argument('lib_id', type=str)
        args = parse.parse_args()
        lib_id = args['lib_id']
        self.response.code = delete_lib(user_id=user_id, lib_id=lib_id)
        return self.response


class GetLib(API):
    """
    查看分类列表, 返回type:0为readlater,1为所有文献,2为普通分类
    """

    @jwt_required
    def post(self):
        user_id = get_jwt_identity()
        self.response = make_response()
        j, c = get_lib(user_id=user_id)
        self.response.code = c
        self.response = jsonify(j)
        return self.response


class GetDocsInLib(API):
    """
    查看分类内容（返回的是这个分类下的文件列表）
    """

    @jwt_required
    def post(self, lib_type):
        user_id = get_jwt_identity()
        self.response = make_response()
        request.get_json(force=True)
        parse = reqparse.RequestParser()
        parse.add_argument('lib_id', type=str)
        args = parse.parse_args()
        lib_id = args['lib_id']
        j, c = get_docs_in_lib(user_id=user_id, lib_id=lib_id, lib_type=int(lib_type))
        self.response.code = c
        self.response = jsonify(j)
        return self.response
