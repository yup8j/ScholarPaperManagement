from backend.test import *

user_id = '5d0f29a33e02f9e99c246717'
lib_name = 'Unit Test'
d_lib_name = 'Del Test'


class TestLibHandler(unittest.TestCase):
    def test_add_lib(self):
        new_lib_id, code = add_lib(user_id=user_id, lib_name=lib_name)
        self.assertEqual(code, 200)
        lib = Library.objects(id=new_lib_id).first()
        self.assertEqual(lib.lib_name, lib_name)