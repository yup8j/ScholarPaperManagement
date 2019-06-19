from mongoengine import *
from flask_restful import Resource
from backend.utils.salt import salt_manager
from hashlib import md5, sha3_256


connect(
    db='test_11',
    host='mongodb://dds-wz9f23f0cffe4b341504-pub.mongodb.rds.aliyuncs.com:3717,dds-wz9f23f0cffe4b342338-pub.mongodb.rds.aliyuncs.com:3717',
    username='root',
    password='qwerty2019()-=',
    authentication_source='admin',
    authentication_mechanism='SCRAM-SHA-1',
    replicaset='mgset-15064123'
)


"""
    下面定义了一些MongoDB数据库中的文档结构
"""
class User(Document):
    _id = StringField()
    username = StringField()
    password_hash = StringField()
    doc_amount = IntField()
    user_type = StringField()

class Metadata(Document):
    title = StringField()
    paper_id = StringField()
    author = ListField()
    publish_date = StringField()
    publish_source = StringField()
    link_url = URLField()
    user_score = IntField()

class Documents(Document):
    _id = StringField()
    owner_id = StringField()
    metadata = EmbeddedDocumentField(Metadata)
    color = IntField()
    topic = ListField()

class Library(Document):
    _id = StringField()
    owner_id = StringField()
    lib_name = StringField()
    doc_list = ListField()

class Topic(Document):
    _id = StringField()
    topic_name = StringField()
    doc_list = ListField()



class API(Resource):
    def __init__(self, db):
        self.db = db
        self.response = None