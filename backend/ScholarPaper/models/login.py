from .required_modules import *
from flask import jsonify
from ScholarPaper.utils.salt import *
from hashlib import md5, sha3_256
import json
import time


class PreLoginAPI(API):
    """
    登录过程的第一次握手
    """
    def __init__(self, db):
        super(PreLoginAPI, self).__init__(db)

    def post(self):
        data = {}
        userInfo = json.loads(str(request.data, encoding='utf-8'))
        uname = userInfo['uname']
        unameQuery = self.db(username=uname)
        if len(unameQuery):
            data['id'] = salt_manager.getNewSalt(uname)
            status_code = 200
        else:
            status_code = 403
        # 构建响应报文
        self.response = make_response(jsonify(data))
        self.response.status_code = status_code
        return self.response


class LoginAPI(API):
    """
    登录过程的第二次握手
    """
    def __init__(self, db):
        super(LoginAPI, self).__init__(db)

    def post(self):
        data = json.loads(str(request.data, encoding='utf-8'))
        uname = data['uname']
        # 用户鉴权，采用与challenge认证类似的方式
        challenge = data['passwd']
        passwdQuery = self.db(username = uname)
        passwd_hash = [row.password_hash for row in passwdQuery]
        salt = salt_manager.matchSalt(uname)
        h_real = None
        if salt:
            h_real = md5()
            h_real.update((passwd_hash[0] + salt).encode('utf-8'))
            # h_real = challenge
        # 生成响应报文
        self.response = make_response()
        if challenge == h_real:
            # 鉴权成功
            if salt_manager.delSalt(uname) == False:
                print("ERROR: Salt Not Exists!")
            self.response.status_code = 200
            timestamp = time.strftime('%Y-%m-%d %a %H:%M:%S', time.localtime(time.time()))
            session_id = sha3_256((uname + timestamp + salt).encode('utf-8'))
            self.response.set_cookie(
                'JSESSIONID', session_id.hexdigest(),
                path='/docollect/',
                httponly=True,
                max_age=3600
            )
        else:
            # 鉴权失败
            self.response.status_code = 403
        return self.response
