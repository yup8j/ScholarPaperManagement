from backend.test import *


class TestColorHandler(unittest.TestCase):
    def test_change_color(self):
        document_id = '5d0f2fa43e02f9e99c246721'
        self.assertEqual(change_color('', '5d0f2fa43e02f9e99c246721', 2), 200)
        doc = Documents.objects(id=document_id).first()
        self.assertEqual(doc.color, 2)
