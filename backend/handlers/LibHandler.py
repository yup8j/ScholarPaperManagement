from backend.models.db_models import Library, User


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
        code =403
    return code