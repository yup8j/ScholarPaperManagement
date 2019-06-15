from flask import Flask, json, request, make_response, jsonify
from flask_restful import Resource
from backend.handlers import LoginHandler
from backend.models.db_models import API

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
        data = json.loads(str(request.data, encoding='utf-8'))
        self.response = make_response()
        if data:
            uname = data['uname']
            challenge = data['passwd']
            session_id, status_code = LoginHandler.LogHandler(uname=uname, challenge=challenge)
            if session_id:
                self.response.set_cookie(
                    'JSESSIONID', session_id.hexdigest(),
                    path='/docollect/',
                    httponly=True,
                    max_age=3600
                )
            self.response.status_code = status_code
            return self.response
