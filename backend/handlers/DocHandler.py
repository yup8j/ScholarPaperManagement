from backend.handlers import *
from backend.utils.call_metadata import get_metadata
from backend.models.db_models import Documents,Library

executor = ThreadPoolExecutor(4)


def upload(stream, user_id, user_name):
    time_stamp = str(int(time.time()))
    name = user_name + '_' + time_stamp
    now_path = user_id + '/' + name + '.pdf'
    try:
        bucket.put_object(now_path, stream)
        code = 200
    except Exception as e:
        print("异常：{}".format(str(e)))
        code = 403
    if code == 200:
        doc_id = executor.submit(get_metadata, user_id, stream, name).result()
        if doc_id == 'Full' or doc_id == 'Error':
            code = 403
        return {"id": str(doc_id)}, code
    else:
        return "", code


def download(document_id, user_id):
    doc_name = Documents.objects(id=str(document_id)).first().save_name
    object_stream = bucket.get_object(user_id + '/' + doc_name + '.pdf')
    return doc_name, object_stream


def delete_document(document_id, user_id):
    delete_doc = Documents.objects(id=str(document_id)).first()
    doc_name = delete_doc.save_name
    doc_id = delete_doc.id
    topic_id = delete_doc.topic
    lib_id = delete_doc.lib
    user = User.objects(id=user_id).first()
    user_doc_amount = user.doc_amount
    user_doc_amount -= 1
    user.update(doc_amount=user_doc_amount)
    try:
        for topic in topic_id:
            delete_topic = Topic.objects(id=str(topic))
            delete_topic.update_one(pull__doc_list=doc_id)
    except Exception as e:
        print(str(e))
    try:
        for lib in lib_id:
            delete_lib = Library.objects(id=lib)
            delete_lib.update_one(pull__doc_list=doc_id)
    except Exception as e:
        print(str(e))
    delete_doc.delete()
    try:
        bucket.delete_object(user_id + '/' + doc_name + '.pdf')
        code = 200
    except Exception as e:
        print(str(e))
        code = 403
    return code
