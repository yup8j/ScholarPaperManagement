from backend.models.db_models import Documents
from backend.models.db_models import Metadata, Topic
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
#
# new_metadata = Metadata()
# new_doc = Documents(owner_id='5cf0c31890f43a4e53492b34', save_name='testname_123456')
# new_metadata.title = 'Microalgal biomass production as a sustainable feedstock for biodiesel: Current status and perspectives'
# new_metadata.paper_id = 'doi:10.1016/j.rser.2016.06.056'
# new_metadata.author = ['Abd El-Fatah Abomohra', 'Wenbiao Jin', 'Renjie Tu', 'Song-Fang Han', 'Mohammed Suleiman Eid',
#                        'Hamed Eladel']
# new_metadata.publish_date = '2016'
# new_metadata.link_url = 'https://www.semanticscholar.org/paper/86263f0756e33c0e2f29e61df9b18f45224c20ad'
# new_metadata.user_score = 0
# new_doc.metadata = new_metadata
# new_doc.save()
# topic = ['Biomass', 'test_topic']
# a = Topic.objects.get(topic_name=topic[0])
# print(a._id)

tid = '5d08e6fca8ef51901b618696'

a = Topic.objects(id=tid).first()
print(a.topic_name)
