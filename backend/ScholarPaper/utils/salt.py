#-*-coding:utf-8 -*-
import random
import string


def generateRandomStr(len):
    strList = [random.choice(string.digits + string.ascii_letters) for i in range(len)]
    randomStr = "".join(strList)
    return randomStr

class Salt:
    def __init__(self):
        self.salt_list = {}

    def getNewSalt(self, tag):
        # 生成长度随机的salt
        salt_len = random.randint(4, 64)
        new_salt = generateRandomStr(salt_len)
        self.salt_list[tag] = new_salt
        return new_salt

    def matchSalt(self, tag):
        if tag in self.salt_list:
            return self.salt_list[tag]
        else:
            return None

    def delSalt(self, tag):
        if tag in self.salt_list:
            del self.salt_list[tag]
            return True
        else:
            return False

salt_manager = Salt()