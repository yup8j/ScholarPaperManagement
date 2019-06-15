from mongoengine import *
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
    password_query = User.objects(username=uname)
    password_hash = [row.password_hash for row in password_query]
    salt = salt_manager.matchSalt(uname)
    h_real = None
    if salt:
        h_real = md5()
        h_real.update((password_hash[0]+salt).encode('utf-8'))

    if challenge == h_real:
        if not salt_manager.delSalt(uname):
            print("Error: Salt Not Exists")
        status_code = 200
        timestamp = time.strftime('%Y-%m-%d %a %H:%M:%S', time.localtime(time.time()))
        session_id = sha3_256((uname + timestamp + salt).encode('utf-8'))
    else:
        status_code = 403
        session_id = ''
    return session_id, status_code