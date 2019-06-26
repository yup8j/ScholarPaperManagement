from backend.handlers.LibHandler import *
from python_wrap_cases import wrap_case
import unittest


test_user_id = '5d0e409366cb169b8fd4338b'   # iwannabetheguy
test_doc_id = '5d0e49b366cb169b8fd433af'    # Automatic Academic Paper Rating Based on Modularized Hierarchical Convolutional Neural Network
test_lib_id = '5d0e6d6ebe0e70cfe16257f3'    # 自然语言

@wrap_case
class TestReadLaterModule(unittest.TestCase):

    ## TODO ##待补充：get_read_later的异常流测试用例
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


@wrap_case
class TestLibModule(unittest.TestCase):

    ## TODO ##待补充：其他lib接口

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


if __name__ == '__main__':
    unittest.main()