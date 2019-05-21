from flask import Flask, request
from flask_restful import Api, Resource
from utils import *
from xjson import *
from model import *
import hashlib
import json


app = Flask(__name__)
api = Api(app)
database.connect()

saltList = {}
paperfile_root = "/"


class Main(Resource):
    def post(self):
        return 1

class PreLoginAPI(Resource):
    def post(self):
        data = {}
        userInfo = json.loads(request.get_data())
        uname = userInfo['uname']
        unameQuery = User.select(User.username).where(User.username == uname)
        if len(unameQuery) > 0:
            msg = 'user found'
            # 生成长度随机的salt
            saltLen = random.randint(4, 64)
            salt = generateRandomStr(saltLen)
            data['id'] = salt
            saltList[uname] = salt
            return json_result(StatusCode.ok, msg, data)
        else:
            msg = 'user not exists'
            return json_result(StatusCode.forbidden, msg)

class LoginAPI(Resource):
    def post(self):
        data = json.loads(request.get_data())
        uname = data['uname']
        challenge = data['challenge']
        passwdQuery = User.select(User.passwd).where(User.username == uname)
        passwd_hash = passwdQuery[0]['passwd']
        h_real = hashlib.md5(passwd_hash + saltList[uname])
        if challenge == h_real:
            pop_ret = saltList.pop(uname)
            return 1
        else:
            msg = 'Password does not match'
            return json_result(StatusCode.forbidden, msg)


api.add_resource(PreLoginAPI, '/login1')
api.add_resource(LoginAPI, '/login2')


if __name__ == '__main__':
    app.run(port=10086, debug=True)
