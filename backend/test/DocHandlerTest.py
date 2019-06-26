from backend.test import *


class TestDocHandler(unittest.TestCase):
    def test_delete(self):
        self.assertEqual(delete_document(document_id='5d0f2f7c3e02f9e99c246720', user_id='5d0f29a33e02f9e99c246717'),
                         200)
