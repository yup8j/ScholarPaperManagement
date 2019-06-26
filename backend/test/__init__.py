import unittest
from backend.handlers.DocHandler import *
import pdfminer
from mongoengine import connect

connect(
    db='test_11',
    host='mongodb://dds-wz9f23f0cffe4b341504-pub.mongodb.rds.aliyuncs.com:3717,dds-wz9f23f0cffe4b342338-pub.mongodb.rds.aliyuncs.com:3717',
    username='root',
    password='qwerty2019()-=',
    authentication_source='admin',
    authentication_mechanism='SCRAM-SHA-1',
    replicaset='mgset-15064123'
)
