from backend.models.db_models import Library, User, Documents
import json


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
