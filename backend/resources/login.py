from backend.resources import *
from backend.handlers.LoginHandler import *
from backend.models.db_models import User
from flask_jwt_extended import (JWTManager, create_access_token, set_access_cookies, \
                                get_jwt_identity, get_raw_jwt)

''' 鉴权模块的初始化 '''
jwt = JWTManager()
blacklist = set()


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist


class PreLoginAPI(API):
    """
    登录过程的第一次握手
    """

    def post(self):
        userInfo = json.loads(str(request.data, encoding='utf-8'))
        if userInfo:
            j, c = PreLoginHandler(userInfo=userInfo)
            self.response = make_response(jsonify(j))
            self.response.status_code = c
        else:
            self.response = make_response()
            self.response.status_code = 403

        return self.response


class LoginAPI(API):
    """
    登录过程的第二次握手
    """

    def post(self):
        ''' 获取参数 '''
        request.get_json(force=True)
        parse = reqparse.RequestParser()
        parse.add_argument('username', type=str)
        parse.add_argument('passwd', type=str)
        args = parse.parse_args()
        uname = args['username']
        challenge = args['passwd']

        content, code, msg = LogHandler(uname=uname, challenge=challenge)
        ''' 生成响应报文 '''
        self.response = make_response()
        if content == None:
            # 错误内容返回
            resp = jsonify({
                "message": msg
            })
            self.response = resp
            self.response.status_code = code
        else:
            # 生成token并设置响应的cookie
            userid = content['userid']
            access_token = create_access_token(identity=userid)
            set_access_cookies(self.response, access_token)
            self.response.status_code = code

        return self.response


class RegisterAPI(API):
    """
    注册过程
    """

    def post(self):
        ''' 获取参数 '''
        request.get_json(force=True)
        parse = reqparse.RequestParser()
        parse.add_argument('username', type=str)
        parse.add_argument('passwd', type=str)
        args = parse.parse_args()
        uname = args['username']
        passwd_hash = args['passwd']

        msg, code = RegisterHandler(uname, passwd_hash)

        ''' 生成响应报文 '''
        resp = jsonify({'msg': msg})
        self.response = make_response(resp)
        self.response.status_code = code
        return self.response


class LogoutAPI(API):
    """
    登出过程
    """

    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        blacklist.add(jti)
        resp = jsonify({'msg': 'Logout success!'})
        self.response = make_response(resp)
        self.response.status_code = 200
        return self.response


class UpgradeUser(API):
    @jwt_required
    def post(self):
        user_id = get_jwt_identity()
        self.response = make_response()
        self.response.status_code = user_upgrade(user_id=user_id)
        return self.response
