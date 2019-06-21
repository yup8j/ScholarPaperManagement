from ..models.db_models import Documents, Metadata, Topic
from mongoengine import Q


def getInfo(userid, doc_id):
    print("Doc id {}".format(doc_id))
    docQuery = Documents.objects(Q(id=doc_id) & Q(owner_id=userid)).first()
    if docQuery == None:
        print("Document not exists!")
        return None
    else:
        topic_list = docQuery.topic
        topicQueryList = [Topic.objects(id=topic_id).first() for topic_id in topic_list]
        topic_name_list = [query.topic_name for query in topicQueryList]

        return docQuery, \
               ",".join([str(topic_id) for topic_id in topic_list]), \
               ",".join([str(name) for name in topic_name_list])
