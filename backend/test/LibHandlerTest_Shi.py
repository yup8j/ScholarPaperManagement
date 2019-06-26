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
        r_value = {'docs': [{'document_id': '5d0f29ba3e02f9e99c24671b',
                             'title': 'Microalgal biomass production as a sustainable feedstock for biodiesel: Current status and perspectives',
                             'mark': 0, 'fst_author': 'Abd El-Fatah Abomohra', 'source': '', 'year': '2016'},
                            {'document_id': '5d0f2fa43e02f9e99c246721', 'title': 'testname_1561276319', 'mark': 2,
                             'fst_author': '-', 'source': '-', 'year': '-'},
                            {'document_id': '5d0f2fab3e02f9e99c246722', 'title': 'testname_1561276331', 'mark': 0,
                             'fst_author': '-', 'source': '-', 'year': '-'},
                            {'document_id': '5d0f30213e02f9e99c246723', 'title': 'testname_1561276446', 'mark': 0,
                             'fst_author': '-', 'source': '-', 'year': '-'}, {'document_id': '5d0f31b23e02f9e99c246738',
                                                                              'title': 'Deep convolutional neural network for the automated detection and diagnosis of seizure using EEG signals',
                                                                              'mark': 0,
                                                                              'fst_author': 'U. Rajendra Acharya',
                                                                              'source': 'Comp. in Bio. and Med.',
                                                                              'year': '2017'},
                            {'document_id': '5d0f32253e02f9e99c246744',
                             'title': 'Detection of Epileptic Seizure Event and Onset Using EEG', 'mark': 0,
                             'fst_author': 'Nabeel Ahammad', 'source': 'BioMed research international',
                             'year': '2014'}]}
        self.assertEqual(resp, r_value)
