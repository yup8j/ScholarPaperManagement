from backend.handlers.InfoHandler import *
import unittest
import json


class TestInfoModule(unittest.TestCase):

    def setUp(self):
        # Account: admin
        self.user_id = '5d0dc758692c739ffe48cdb4'

    def test_get(self):
        print('\n============== test get ==============')
        # Article: Automatic Academic Paper Rating Based on Modularized Hierarchical Convolutional Neural Network
        doc_id = '5d0dfc54265f039df171b20d'
        Q, t_list, tname_list = getInfo(userid=self.user_id, doc_id=doc_id)

        # 预期返回结果
        metadata = {
            "title": "Automatic Academic Paper Rating Based on Modularized Hierarchical Convolutional Neural Network",
            "paper_id": "arXiv:1805.03977",
            "author": ["Pengcheng Yang", "Xu Sun", "Wei Li", "Shuming Ma"],
            "publish_date": "2018",
            "publish_source": "ACL",
            "link_url": "https://arxiv.org/abs/1805.03977",
            "user_score": 0
        }
        t_res = [
            '5d0a33726694b1cbdc6e55e1',
            '5d0a33726694b1cbdc6e55e2',
            '5d0a33726694b1cbdc6e55e3',
            '5d08e64ba4e85ec656832708',
            '5d0a33726694b1cbdc6e55e5',
            '5d08e64ba4e85ec65683270e',
        ]
        tname_res = [
            'Convolutional neural network',
            'Artificial neural network',
            'HTTPS',
            'Baseline (configuration management)',
            'Social inequality',
            'test_topic',
        ]
        # 输出返回信息
        print('== Metadata ==\n', Q.metadata.to_json())
        print('== t_list ==\n', t_list.split(','))
        print('== t_name ==\n', tname_list.split(','))
        # 判断是否符合预期输出
        self.assertEquals(Q.metadata.to_json(), json.dumps(metadata))
        self.assertEquals(t_list.split(','), t_res)
        self.assertEquals(tname_list.split(','), tname_res)


    def test_edit(self):
        print('\n============== test edit ==============')
        # Article: testname_1561196656
        doc_id = '5d0df87025cbace36f486e6c'
        doc_info = {
            'document_id': doc_id,
            'title': 'testname_2333333333',
            'paper_id': '12345',
            'author': ['a', 'b'],
            'year': '2018',
            'source': 'xxx',
            'link_url': 'https://www.baidu.com',
            'score': '10'
        }
        editInfo(userid=self.user_id, docInfo=doc_info)
        # 查看修改的信息
        Q, t_list, tname_list = getInfo(userid=self.user_id, doc_id=doc_id)
        metadata = {
            'title': 'testname_2333333333',
            'paper_id': '12345',
            'author': ['a', 'b'],
            'publish_date': '2018',
            'publish_source': 'xxx',
            'link_url': 'https://www.baidu.com',
            'user_score': 10
        }
        print('== Metadata ==\n', Q.metadata.to_json())
        self.assertEquals(Q.metadata.to_json(), json.dumps(metadata))


if __name__ == '__main__':
    unittest.main()