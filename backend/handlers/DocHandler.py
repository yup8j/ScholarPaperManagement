import time
from time import sleep
import re
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

executor = ThreadPoolExecutor(2)
rsrcmgr = PDFResourceManager()
sio = StringIO()
codec = 'utf-8'
laparams = LAParams()
device = TextConverter(rsrcmgr, sio, codec=codec, laparams=laparams)
interpreter = PDFPageInterpreter(rsrcmgr, device)


def upload(stream, user_id, user_name):
    time_stamp = str(int(time.time()))
    name = user_name + '_' + time_stamp
    now_path = user_id + '/' + name + '.pdf'
    # get_metadata(user_id,stream)
    #
    # bucket.put_object(now_path, stream)
    executor.submit(get_metadata, user_id, stream)
    sleep(2)


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


def get_metadata(user_id, stream):
    identifier = get_identifier(stream)
    if identifier:
        (key, value), = identifier.items()
        rurl = "http://api.semanticscholar.org/v1/paper/"
        final = "?include_unknown_references=TRUE"
        if key == 'None':
            return
        if key == 'doi':
            rurl = rurl + value + final
        elif key == 'arXiv':
            rurl = rurl + "arXiv:" + value + final
        response = requests.get(url=rurl)
        json_data = json.loads(response.text)
        title = json_data['title']
        paper_id = key + ':' + value
        author = []
        for i in list(json_data['authors']):
            author.append(i['name'])
        publish_date = json_data['year']
        topic = []
        for i in list(json_data['topics']):
            topic.append(i['topic'])
        url = json_data['url']
        print(title, paper_id, author, publish_date, topic, url)
        return json_data
    else:
        # 实在抓不到了
        print("Hello world")
