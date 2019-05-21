#-*-coding:utf-8 -*-
import random
import string


def generateRandomStr(len):
    strList = [random.choice(string.digits + string.ascii_letters) for i in enumerate(len)]
    randomStr = "".join(strList)
    return randomStr



