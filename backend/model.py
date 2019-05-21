from peewee import *

database = MySQLDatabase('scholarpaper', **{'charset': 'utf8', 'use_unicode': True, 'host': 'rm-wz90kc05gqggv6vo5ko.mysql.rds.aliyuncs.com', 'port': 3306, 'user': 'root', 'password': 'SE2019()-='})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class User(BaseModel):
    doc_amount = IntegerField(constraints=[SQL("DEFAULT 0")])
    passwd = CharField(constraints=[SQL("DEFAULT ''")])
    userid = CharField(constraints=[SQL("DEFAULT '0000000-0000-0000-0000-000000000000'")], primary_key=True)
    username = CharField(constraints=[SQL("DEFAULT ''")])
    usertype = CharField(constraints=[SQL("DEFAULT '0'")])

    class Meta:
        table_name = 'user'

class Document(BaseModel):
    document_id = CharField(constraints=[SQL("DEFAULT '0000000-0000-0000-0000-000000000000'")], primary_key=True)
    paper_id = CharField(null=True)
    store_path = CharField(constraints=[SQL("DEFAULT ''")])
    title = TextField()
    userid = ForeignKeyField(column_name='userid', field='userid', model=User)

    class Meta:
        table_name = 'document'

class Docinfo(BaseModel):
    author = TextField()
    document = ForeignKeyField(column_name='document_id', constraints=[SQL("DEFAULT '0000000-0000-0000-0000-000000000000'")], field='document_id', model=Document, primary_key=True)
    link = TextField(null=True)
    score = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    source = CharField(constraints=[SQL("DEFAULT ''")])
    year = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'docinfo'

class Library(BaseModel):
    lib_id = CharField(constraints=[SQL("DEFAULT '0000000-0000-0000-0000-000000000000'")], primary_key=True)
    lib_name = CharField(constraints=[SQL("DEFAULT ''")])
    userid = ForeignKeyField(column_name='userid', field='userid', model=User)

    class Meta:
        table_name = 'library'

class Libdoc(BaseModel):
    document = ForeignKeyField(column_name='document_id', field='document_id', model=Document)
    lib = ForeignKeyField(column_name='lib_id', field='lib_id', model=Library)

    class Meta:
        table_name = 'libdoc'
        indexes = (
            (('lib', 'document'), True),
        )
        primary_key = CompositeKey('document', 'lib')

class Marks(BaseModel):
    document = ForeignKeyField(column_name='document_id', field='document_id', model=Document)
    mark_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    userid = ForeignKeyField(column_name='userid', field='userid', model=User)

    class Meta:
        table_name = 'marks'
        indexes = (
            (('userid', 'document'), True),
        )
        primary_key = CompositeKey('document', 'userid')

class Topic(BaseModel):
    topic_id = CharField(constraints=[SQL("DEFAULT '0000000-0000-0000-0000-000000000000'")], primary_key=True)
    topic_name = CharField(constraints=[SQL("DEFAULT ''")])

    class Meta:
        table_name = 'topic'

class Topicdoc(BaseModel):
    document = ForeignKeyField(column_name='document_id', field='document_id', model=Document)
    topic = ForeignKeyField(column_name='topic_id', field='topic_id', model=Topic)

    class Meta:
        table_name = 'topicdoc'
        indexes = (
            (('document', 'topic'), True),
        )
        primary_key = CompositeKey('document', 'topic')

