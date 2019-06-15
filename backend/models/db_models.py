from flask import request, make_response
from mongoengine import *
from flask_restful import Resource



class User(Document):
    _id = StringField()
    username = StringField()
    password_hash = StringField()
    doc_amount = IntField()
    user_type = StringField()


class Metadata(EmbeddedDocument):
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
    def __init__(self):
        self.response = None
