from backend.models.db_models import User, Library
from backend.utils.salt import salt_manager
from hashlib import md5


def PreLoginHandler(userInfo):
    data = {}
    if 'username' not in userInfo:
        status_code = 404
    else:
        uname = userInfo['username']
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
        h_real = None
        password_hash = userquery.password_hash
        salt = salt_manager.matchSalt(uname)
        a = (password_hash.lower() + salt)
        if salt:
            h_real = md5(a.encode('utf8')).hexdigest()
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


def RegisterHandler(username, password_hash):
    userQuery = User.objects(username=username).first()
    if userQuery == None:
        # 创建新的用户记录
        new_user = User(
            username=username,
            password_hash=password_hash,
            user_type='normal'
        )
        new_user.save()

        # 为新用户创建待读列表
        new_lib = Library(
            owner_id=new_user.id,
            lib_name='待读列表'
        )
        new_lib.save()

        return 'Register Success', 200
    else:
        msg = 'Username exists!'
        return msg, 403


def user_upgrade(user_id):
    try:
        User.objects(id=user_id).update_one(set__user_type='advanced')
        code = 200
    except Exception as e:
        code = 403
    return code