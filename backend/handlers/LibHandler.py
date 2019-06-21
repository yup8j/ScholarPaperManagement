from backend.models.db_models import Library, User, Documents
import json
from mongoengine import Q


def add_lib(user_id, lib_name):
    new_lib = Library(owner_id=user_id, lib_name=lib_name)
    try:
        new_lib.save()
        User.objects(id=user_id).update_one(inc__lib_amount=1)
        code = 200
        new_lib_id = new_lib.id
    except Exception as e:
        print(str(e))
        new_lib_id = ''
        code = 403
    return new_lib_id, code


def delete_lib(user_id, lib_id):
    d_lib = Library.objects(id=lib_id).first()
    try:
        d_lib.delete()
        User.objects(id=user_id).update_one(dec__lib_amount=1)
        code = 200
    except Exception as e:
        print(str(e))
        code = 403
    return code


def get_lib(user_id):
    try:
        lib_query = Library.objects(owner_id=user_id)
        lib_id_list = [str(query.id) for query in lib_query]
        lib_name_list = [query.lib_name for query in lib_query]
        doc_amount_list = [len(query.doc_list) for query in lib_query]
        all_doc = User.objects(id=user_id).first().doc_amount
        type_list = []
        for i in range(len(lib_id_list)):
            if not lib_name_list[i] == '待读列表':
                type_list.append(2)
            else:
                type_list.append(0)
        type_list.append(1)
        doc_amount_list.append(all_doc)
        lib_id_list.append('1')
        lib_name_list.append('全部文献')
        final = [{'lib_id': lib_id, 'lib_name': lib_name, 'doc_count': doc_count, 'type': lib_type} for
                 lib_id, lib_name, doc_count, lib_type in zip(lib_id_list, lib_name_list, doc_amount_list, type_list)]
        my_response = {'libs': final}
        code = 200
    except Exception as e:
        print(e)
        my_response = ''
        code = 403
    return my_response, code


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


def get_docs_in_lib(user_id, lib_id, lib_type):
    if not lib_type == 1:
        lib_query = Library.objects(id=lib_id).first()
        list_of_doc = [str(i) for i in lib_query.doc_list]
        title_list = []
        mark_list = []
        fst_author_list = []
        source_list = []
        publish_year_list = []
        for doc_id in list_of_doc:
            doc_query = Documents.objects(id=doc_id).first()
            title_list.append(doc_query.metadata.title)
            mark_list.append(doc_query.color)
            try:
                fst_author_list.append(doc_query.metadata.author[0])
            except Exception as e:
                print(str(e))
                fst_author_list.append('-')
            source_list.append(doc_query.metadata.publish_source)
            try:
                publish_year_list.append(doc_query.metadata.publish_date)
            except Exception as e:
                print(e)
                publish_year_list.append('-')
        final = [{'document_id': d_id, 'title': title, 'mark': mark, 'fst_author': fst_author, 'source': source,
                  'year': year} for
                 d_id, title, mark, fst_author, source, year in
                 zip(list_of_doc, title_list, mark_list, fst_author_list, source_list, publish_year_list)]
        my_response = {'docs': final}
        print(my_response)
        return my_response, 200
    else:
        doc_query = Documents.objects(owner_id=user_id)
        list_of_doc = [str(query.id) for query in doc_query]
        title_list = []
        mark_list = []
        fst_author_list = []
        source_list = []
        publish_year_list = []
        for doc_id in list_of_doc:
            doc_query = Documents.objects(id=doc_id).first()
            title_list.append(doc_query.metadata.title)
            mark_list.append(doc_query.color)
            try:
                fst_author_list.append(doc_query.metadata.author[0])
            except Exception as e:
                print(str(e))
                fst_author_list.append('-')
            source_list.append(doc_query.metadata.publish_source)
            try:
                publish_year_list.append(doc_query.metadata.publish_date)
            except Exception as e:
                print(e)
                publish_year_list.append('-')
        final = [{'document_id': d_id, 'title': title, 'mark': mark, 'fst_author': fst_author, 'source': source,
                  'year': year} for
                 d_id, title, mark, fst_author, source, year in
                 zip(list_of_doc, title_list, mark_list, fst_author_list, source_list, publish_year_list)]
        my_response = {'docs': final}
        return my_response, 200


def get_read_later(user_id):
    try:
        lib_query = Library.objects(Q(lib_name="待读列表") & Q(owner_id=user_id)).first()
        j, c = get_docs_in_lib(user_id=user_id, lib_id=lib_query.id, lib_type=0)
        return j, c
    except Exception as e:
        print(str(e))
        return '', 403
