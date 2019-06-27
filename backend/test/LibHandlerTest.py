from backend.test import *
from python_wrap_cases import wrap_case


# test scene 1
user_id = '5d0f29a33e02f9e99c246717'
lib_name = 'Unit Test'
d_lib_name = 'Del Test'

# test scene 2
test_user_id = '5d0e409366cb169b8fd4338b'   # iwannabetheguy
test_doc_id = '5d0e4a7d66cb169b8fd433b6'    # Academic Paper Rating
test_lib_id = '5d0e6d6ebe0e70cfe16257f3'    # 自然语言


@wrap_case
class TestLibHandler(unittest.TestCase):
    def test_add_lib(self):
        new_lib_id, code = add_lib(user_id=user_id, lib_name=lib_name)
        self.assertEqual(code, 200)
        lib = Library.objects(id=new_lib_id).first()
        self.assertEquals(lib.lib_name, lib_name)
        delete_lib(user_id=user_id, lib_id=lib.id)

    def test_delete_lib(self):
        new_lib_id, code = add_lib(user_id=user_id, lib_name=d_lib_name)
        d_lib = Library.objects(id=new_lib_id).first()
        self.assertEqual(delete_lib(user_id=user_id, lib_id=d_lib.id), 200)

    def test_get_lib(self):
        resp, code = get_lib(user_id=user_id)
        self.assertEqual(code, 200)

    @wrap_case('1', 1)
    @wrap_case('5d0f29a33e02f9e99c246718', 0)
    @wrap_case('5d12e9b3902096ec18b637f5', 2)
    def test_get_docs(self, libid, type):
        resp, code = get_docs_in_lib(user_id=user_id, lib_id=libid, lib_type=type)
        self.assertEqual(code, 200)

    @wrap_case(test_doc_id, test_lib_id, test_user_id, 200)
    def test_add_docs(self, docid, libid, userid, code):
        j, c = add_to_lib(document_id=docid, lib_id=libid, user_id=userid)
        print('message: {}, code: {}'.format(j, c))
        self.assertEqual(c, code)

    @wrap_case(test_doc_id, test_lib_id, test_user_id, 200)
    def test_remove_docs(self, docid, libid, userid, code):
        j, c = remove_from_lib(document_id=docid, lib_id=libid, user_id=userid)
        print('message: {}, code: {}'.format(j, c))
        self.assertEqual(c, code)


@wrap_case
class TestReadLaterModule(unittest.TestCase):

    @wrap_case(test_user_id, 200)
    def test_get(self, userid, code):
        j, c = get_read_later(user_id=userid)
        print('data: {}, code: {}'.format(j, c))
        self.assertEqual(c, code)

    @wrap_case(test_doc_id, test_user_id, 200)
    def test_add(self, docid, userid, code):
        j, c = add_read_later(document_id=docid, user_id=userid)
        print('data: {}, code: {}'.format(j, c))
        self.assertEqual(c, code)

    @wrap_case(test_doc_id, test_user_id, 200)
    def test_remove(self, docid, userid, code):
        j, c = remove_from_read_later(document_id=docid, user_id=userid)
        print('data: {}, code: {}'.format(j, c))
        self.assertEqual(c, code)


if __name__ == '__main__':
    unittest.main()