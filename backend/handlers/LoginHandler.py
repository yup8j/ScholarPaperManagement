from backend.models.db_models import User
from backend.utils.salt import salt_manager
from hashlib import md5, sha3_256
import time


def PreLoginHandler(userInfo):
    data = {}
    uname = userInfo['uname']
    unameQuery = User.objects(username=uname)
    if len(unameQuery):
        data['id'] = salt_manager.getNewSalt(uname)
        status_code = 200
    else:
        status_code = 403

    return data, status_code


def LogHandler(uname, challenge):
    content = {}
    userquery = User.objects(username=uname).first()
    if userquery == None:
        # 无结果返回
        message = 'Oops! User not found...'
        status_code = 403
        content = None
    else:
        password_hash = userquery.password_hash
        salt = salt_manager.matchSalt(uname)
        h_real = None
        if salt:
            h_real = md5((password_hash + salt).encode('utf-8')).hexdigest()
            print(h_real)

        # challenge = h_real  # 应用时请注释！
        if challenge == h_real:
            # 认证成功
            if not salt_manager.delSalt(uname):
                print("Error: Salt Not Exists")
            status_code = 200
            message = 'Verification success! '
            content['userid'] = str(userquery.id)
        else:
            # 密码验证错误，认证失败
            status_code = 403
            message = 'Password verification failed! '
            content = None
    return content, status_code, message
