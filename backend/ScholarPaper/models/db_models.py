from flask import request, make_response
from mongoengine import *
from flask_restful import Resource


connect(
    db='test_11',
    host='mongodb://dds-wz9f23f0cffe4b341504-pub.mongodb.rds.aliyuncs.com:3717,dds-wz9f23f0cffe4b342338-pub.mongodb.rds.aliyuncs.com:3717',
    username='root',
    password='qwerty2019()-=',
    authentication_source='admin',
    authentication_mechanism='SCRAM-SHA-1',
    replicaset='mgset-15064123'
)


class User(Document):
    _id = StringField()
    username = StringField()
    password_hash = StringField()
    doc_amount = IntField()
    user_type = StringField()


class API(Resource):
    def __init__(self, db):
        self.db = db
        self.response = None