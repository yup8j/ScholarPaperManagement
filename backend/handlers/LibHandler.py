from backend.models.db_models import Library, User, Documents
import json
from mongoengine import Q


def add_lib(user_id, lib_name):
    """
    添加新的分类列表
    """
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
    """
    删除已有的分类列表
    """
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
    """
    获取当前用户的所有分类列表
    """
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


def get_docs_in_lib(user_id, lib_id, lib_type):
    """
    获取某个分类列表下的所有文献
    """
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
    """
    获取待读列表下的所有文献
    """
    try:
        lib_query = Library.objects(Q(lib_name="待读列表") & Q(owner_id=user_id)).first()
        j, c = get_docs_in_lib(user_id=user_id, lib_id=lib_query.id, lib_type=0)
        return j, c
    except Exception as e:
        print(str(e))
        return '', 403


def add_to_lib(document_id, lib_id, user_id):
    """
    将选中文献添加至选中的分类中
    """
    doc_query = Documents.objects(Q(id=document_id)).first()
    doc_query.update(push__lib=lib_id)

    lib_query = Library.objects(Q(id=lib_id) & Q(owner_id=user_id)).first()
    lib_query.update(push__doc_list=document_id)
    return 'add success', 200


def remove_from_lib(document_id, lib_id, user_id):
    """
    将选中文献从分类中移除
    """
    doc_query = Documents.objects(Q(id=document_id))
    doc_query.update_one(pull__lib=lib_id)

    lib_query = Library.objects(Q(id=lib_id) & Q(owner_id=user_id))
    lib_query.update_one(pull__doc_list=document_id)
    return 'remove success', 200


def add_read_later(document_id, user_id):
    try:
        lib_query = Library.objects(Q(lib_name="待读列表") & Q(owner_id=user_id)).first()
        j, c = add_to_lib(document_id=document_id, lib_id=lib_query.id, user_id=user_id)
        return j, c
    except Exception as e:
        print(str(e))
        return '', 403


def remove_from_read_later(document_id, user_id):
    try:
        lib_query = Library.objects(Q(lib_name="待读列表") & Q(owner_id=user_id)).first()
        j, c = remove_from_lib(document_id=document_id, lib_id=lib_query.id, user_id=user_id)
        return j, c
    except Exception as e:
        print(str(e))
        return '', 403
