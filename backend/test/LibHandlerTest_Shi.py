from backend.test import *

user_id = '5d0f29a33e02f9e99c246717'
lib_name = 'Unit Test'
d_lib_name = 'Del Test'


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

    def test_get_docs(self):
        resp, code = get_docs_in_lib(user_id=user_id, lib_id='1', lib_type=1)
        self.assertEqual(code, 200)

if __name__ == '__main__':
    unittest.main()