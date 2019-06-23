import time
from time import sleep
import re
import mongoengine
from io import BufferedReader
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter  # process_pdf
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import StringIO
import pdfx
from pdfminer import pdfparser, pdfdocument, pdftypes, converter
from backend.utils.oss import *
import requests
import json
from concurrent.futures import ThreadPoolExecutor
from backend.models.db_models import Documents, Topic, User
from backend.models.db_models import Metadata

doi_pattern = re.compile("\\b(10[.][0-9]{4,}(?:[.][0-9]+)*/(?:(?![\"&\'<>])\S)+)\\b")

vixra_regex = r"""\[\s?([^\s,]+):viXra"""


def get_doi(instr):
    """
    返回DOI
    :param instr: MetaData（大部分期刊均有）
    :return: doi，形如 '10.1371/journal.pcbi.1004697'
    """
    match = doi_pattern.search(instr)
    if match:
        return match.group()
    else:
        return


def get_identifier(stream):
    """
    返回文献标示符
    :return: 标示类型和值，例如'{'arXiv': '1805.03977'}, {'doi': '10.1016/j.rser.2016.06.056'}, {'None': ''}'
    """
    identifier = {}
    rsrcmgr = PDFResourceManager()
    sio = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, sio, codec=codec, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    pdf_stream = pdfparser.PDFParser(stream)
    doc = pdfdocument.PDFDocument(pdf_stream, caching=True)
    if 'Metadata' in dict(doc.catalog).keys():
        metadata = pdftypes.resolve1(doc.catalog['Metadata']).get_data().decode()
        if get_doi(metadata):
            identifier['doi'] = get_doi(metadata)
        else:
            identifier['None'] = ""
    else:
        try:
            stream = BufferedReader(stream._file)
            for page in PDFPage.get_pages(stream):
                interpreter.process_page(page)
            text = sio.getvalue()
            line = text
            line = line.replace(' ', '')
            line = line.replace('\n', '')
            res = re.findall(vixra_regex, line, re.IGNORECASE)
            if res:
                arxiv_id = list(set([r.strip(".") for r in res]))[0][::-1]
                arxiv_id = re.sub(r'v([0-9])', '', arxiv_id)
                identifier['arXiv'] = arxiv_id
            else:
                identifier['None'] = ""
        except:
            return ""
    return identifier


def get_metadata(user_id, stream, name):
    identifier = get_identifier(stream)
    if identifier:
        (key, value), = identifier.items()
        rurl = "http://api.semanticscholar.org/v1/paper/"
        final = "?include_unknown_references=TRUE"
        if key == 'None':
            try:
                user = User.objects(id=user_id).first()
                user_type = user.user_type
                user_doc_amount = user.doc_amount
                user_doc_amount += 1
                if not user_type == 'advanced':
                    if user_doc_amount > 10:
                        return 'Full'
                user.update(doc_amount=user_doc_amount)
                new_document = Documents(owner_id=user_id, save_name=name, color=0, save_note=0)
                new_metadata = Metadata(title=str(name), user_score=0, paper_id='-', publish_date='-',
                                        publish_source='-')
                new_document.metadata = new_metadata
                new_document.save()
                return new_document.id
            except Exception as e:
                print(str(e))
        url = ''
        if key == 'doi':
            url = 'https://dx.doi.org/' + value
            rurl = rurl + value + final
        elif key == 'arXiv':
            url = 'https://arxiv.org/abs/' + value
            rurl = rurl + "arXiv:" + value + final
        response = requests.get(url=rurl)
        json_data = json.loads(response.text)
        if 'error' in dict(json_data):
            try:
                user = User.objects(id=user_id).first()
                user_type = user.user_type
                user_doc_amount = user.doc_amount
                user_doc_amount += 1
                if not user_type == 'advanced':
                    if user_doc_amount > 10:
                        return 'Full'
                user.update(doc_amount=user_doc_amount)
                new_document = Documents(owner_id=user_id, save_name=name, color=0, save_note=0)
                new_metadata = Metadata(title=str(name), user_score=0, paper_id='-', author=['-'], publish_date='-',
                                        publish_source='-', link_url='-')
                new_document.metadata = new_metadata
                new_document.save()
                return new_document.id
            except Exception as e:
                print(str(e))
        title = json_data['title']
        try:
            source = json_data['venue']
        except Exception as e:
            print(str(e))
            source = '-'
        paper_id = key + ':' + value
        author = []
        for i in list(json_data['authors']):
            author.append(i['name'])
        try:
            publish_date = json_data['year']
        except Exception as e:
            print(str(e))
            publish_date = '-'
        topic = []
        topic_id = []
        for i in list(json_data['topics']):
            topic.append(i['topic'])
        topic.append("test_topic")
        # user_info
        user = User.objects(id=user_id).first()
        user_type = user.user_type
        user_doc_amount = user.doc_amount
        user_doc_amount += 1
        if not user_type == 'advanced':
            if user_doc_amount > 10:
                return 'Full'
        user.update(doc_amount=user_doc_amount)
        for one_topic in topic:
            try:
                Topic(topic_name=one_topic).save()
            except mongoengine.errors.NotUniqueError:
                continue
        for one_topic in topic:
            topic_id.append(str(Topic.objects.get(topic_name=one_topic).id))
        # document
        new_metadata = Metadata(title=title, paper_id=paper_id, author=author, publish_date=str(publish_date),
                                publish_source=source, link_url=url, user_score=0)
        new_document = Documents(owner_id=user_id, metadata=new_metadata, color=0, topic=topic_id, save_name=name,
                                 save_note=0)
        new_document.save()
        new_document_id = new_document.id
        # 回到topic插入
        for tid in topic_id:
            Topic.objects(id=tid).update_one(push__doc_list=new_document_id)
        return new_document_id
    else:
        return 'Error'
