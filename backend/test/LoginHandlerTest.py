from backend.handlers.LoginHandler import *
from python_wrap_cases import wrap_case
from hashlib import md5
import unittest


@wrap_case
class TestPreLoginModule(unittest.TestCase):

    @wrap_case({'input': {'username': 'admin'}, 'code': 200})
    @wrap_case({'input': {'username': 'xxx'}, 'code': 403})
    @wrap_case({'input': {'uname': 'admin'}, 'code': 404})
    def test_sample(self, param=None):
        j, c = PreLoginHandler(param['input'])
        print('code: {}, data: {}'.format(c, j))
        self.assertEqual(c, param['code'])


@wrap_case
class TestLoginModule(unittest.TestCase):

    @wrap_case({'name': 'admin', 'password': '123456', 'code': 200})
    @wrap_case({'name': '123', 'password': '123456', 'code': 403})
    @wrap_case({'name': 'admin', 'password': '12345', 'code': 403})
    def test_sample(self, param):
        j, c = PreLoginHandler({'username': 'admin'})
        salt = j['id']
        password_hash = md5(param['password'].encode('utf8')).hexdigest()
        j, c, m = LogHandler(
            uname=param['name'],
            challenge=md5((password_hash + salt).encode('utf8')).hexdigest()
        )
        print('data: {}\ncode: {}\nmessage: {}'.format(j, c, m))
        self.assertEqual(c, param['code'])


@wrap_case
class TestRegisterModule(unittest.TestCase):

    # 想测试此用例，需输入一个没被使用过的username
    # @wrap_case({'username': 'User', 'password': 'asdfghjkl;', 'code': 200})
    @wrap_case({'username': 'User', 'password': 'qwerty', 'code': 403})
    def test_sample(self, param):
        name = param['username']
        password = md5(param['password'].encode('utf8')).hexdigest()
        m, c = RegisterHandler(name, password)
        print('message: {}, code: {}'.format(m, c))
        self.assertEqual(c, param['code'])


if __name__ == '__main__':
    unittest.main()