from flask import  jsonify

class StatusCode(object):
    ok = 200
    paramsError = 400
    unauth = 401
    forbidden = 403
    methodError = 405
    servererror = 500


def json_result(code, message, data={}):
    return jsonify({"code": code, "message":message, "data":data})


def json_success(message='', data=None):
    return json_result(code=StatusCode.ok, message=message, data=data)


def json_params_error(message='', data=None):
    """
     请求参数错误
    """
    return json_result(code=StatusCode.paramsError, message=message, data=data)

def json_unauth_error(message='', data=None):
    """
    没有权限访问
    """
    return json_result(code=StatusCode.unauth, message=message, data=data)

def json_method_error(message='', data=None):
    """
    请求方法错误
    """
    return json_result(code=StatusCode.methodError, message=message, data=data)

def json_server_error(message='', data=None):
    """
    服务器内部错误
    """
    return json_result(code=StatusCode.servererror, message=message, data=data) 