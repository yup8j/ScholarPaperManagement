from backend.test import *


class TestNoteHandler(unittest.TestCase):
    def test_get_note(self):
        content, code = get_note(document_id='5d0f2fa43e02f9e99c246721', user_id='5d0f29a33e02f9e99c246717')
        self.assertEqual(code, 200)
        content, code = get_note(document_id='5d0f2fa43e01f9e99c246721', user_id='5d0f29a33e02f9e99c246717')
        self.assertEqual(code, 403)

    def test_save_note(self):
        code = save_note(document_id='5d0f2fa43e02f9e99c246721', user_id='5d0f29a33e02f9e99c246717',
                         note_content='Hello, world')
        self.assertEqual(code, 200)
        content, code = get_note(document_id='5d0f2fa43e02f9e99c246721', user_id='5d0f29a33e02f9e99c246717')
        self.assertEqual(content, 'Hello, world')
        self.assertEqual(code, 200)
        code = save_note(document_id='5d0f2fa43e02f8e99c246721', user_id='5d0f29a33e02f9e99c246717',
                         note_content='Hello, world')
        self.assertEqual(code, 403)