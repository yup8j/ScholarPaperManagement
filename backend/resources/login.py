from backend.resources import *
from backend.models.db_models import User
from flask_jwt_extended import (JWTManager,create_access_token, create_refresh_token, \
                                get_jwt_identity, set_access_cookies, set_refresh_cookies, \
                                unset_jwt_cookies, jwt_refresh_token_required)


jwt = JWTManager()
user = User()


class PreLoginAPI(API):
    """
    登录过程的第一次握手
    """

    def post(self):
        userInfo = json.loads(str(request.data, encoding='utf-8'))
        if userInfo:
            j, c = LoginHandler.PreLoginHandler(userInfo=userInfo)
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
        self.response = make_response()
        ''' 获取参数 '''
        payload = request.get_json(force=True)
        parse = reqparse.RequestParser()
        parse.add_argument('uname', type=str)
        parse.add_argument('passwd', type=str)
        args = parse.parse_args()
        uname = args['uname']
        challenge = args['passwd']
        content, code, msg = LoginHandler.LogHandler(uname=uname, challenge=challenge)

        ''' 生成响应报文 '''
        if content == None:
            # 错误内容返回
            resp = jsonify({
                "status_code": code,
                "message": msg
            })
            self.response = resp
        else:
            # 生成token并设置响应的cookie
            userid = content['userid']
            access_token = create_access_token(identity=userid)
            set_access_cookies(self.response, access_token)
            self.response.status_code = code

        return self.response


class TokenRefresh(Resource):
   @jwt_refresh_token_required
   def post(self):
       try:
           current_user = get_jwt_identity()
           JSESSIONID = create_access_token(identity=current_user)
           resp = jsonify({'message': 'Token Refreshed!'})
           set_access_cookies(resp, JSESSIONID)
           return resp
       except:
           return jsonify({'error': 'Something went wrong refreshing token'})