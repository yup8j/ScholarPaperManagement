from backend.test import *
import oss2
from backend.utils.call_metadata import get_identifier

auth = oss2.Auth('LTAI6huPFcsniRHT', 'Qo7kumR85OhK6nbez0IVKyTWYX4Beq')
bucket = oss2.Bucket(auth, 'oss-cn-shenzhen.aliyuncs.com', 'bucket-for-2019-hitsz')


class TestDelete(unittest.TestCase):
    def test_delete(self):
        self.assertEqual(delete_document(document_id='5d0f2f7c3e02f9e99c246720', user_id='5d0f29a33e02f9e99c246717'),
                         200)


class UploadTest(unittest.TestCase):
    def test_upload(self):
        f = open('doi.pdf', 'rb')
        a = bucket.put_object('Unittest.pdf', f)
        f.close()
        self.assertEqual(type(a), oss2.models.PutObjectResult)


class GetIdentifierTest(unittest.TestCase):
    def test_get_id(self):
        identifier = {'doi': '10.1016/j.patcog.2012.09.005'}
        f1 = open('doi.pdf', 'rb')
        j = get_identifier(f1)
        f1.close()
        self.assertEqual(j, identifier)


if __name__ == '__main__':
    unittest.main()
