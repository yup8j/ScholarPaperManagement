from mongoengine import *
from flask_restful import Resource


class User(Document):
    username = StringField()
    password_hash = StringField()
    doc_amount = IntField(default=0)
    lib_amount = IntField(default=0)
    user_type = StringField()


class Metadata(EmbeddedDocument):
    title = StringField()
    paper_id = StringField()
    author = ListField(StringField())
    publish_date = StringField()
    publish_source = StringField()
    link_url = URLField()
    user_score = IntField()


class Documents(Document):
    owner_id = ObjectIdField()
    metadata = EmbeddedDocumentField(Metadata)
    color = IntField()
    topic = ListField(ObjectIdField())
    save_name = StringField()
    save_note = IntField()
    lib = ListField(ObjectIdField())


class Library(Document):
    owner_id = StringField()
    lib_name = StringField()
    doc_list = ListField(ObjectIdField())


class Topic(Document):
    topic_name = StringField(unique=True)
    doc_list = ListField(ObjectIdField())


class API(Resource):
    def __init__(self):
        self.response = None
