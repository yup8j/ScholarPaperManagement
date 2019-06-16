import time
from time import sleep
from backend.utils.oss import *
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(2)


def upload(stream, user_id, user_name):
    time_stamp = str(int(time.time()))
    name = user_name + '_' + time_stamp
    now_path = user_id + '/' + name + '.pdf'
    executor.submit(get_metadata, user_id, stream)
    # bucket.put_object(now_path, stream)
    sleep(1)
    return 1


import re

import pdfx
from pdfminer import pdfparser, pdfdocument, pdftypes, converter

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
    pdf_stream = pdfparser.PDFParser(stream)
    doc = pdfdocument.PDFDocument(pdf_stream, caching=True)
    if 'Metadata' in dict(doc.catalog).keys():
        metadata = pdftypes.resolve1(doc.catalog['Metadata']).get_data().decode()
        if get_doi(metadata):
            identifier['doi'] = get_doi(metadata)
        else:
            identifier['None'] = ""
    else:
        pdf_x = pdfx.PDFx(stream)
        line = pdf_x.get_text()
        line = line.replace(' ', '')
        line = line.replace('\n', '')

        res = re.findall(vixra_regex, line, re.IGNORECASE)
        if res:
            arxiv_id = list(set([r.strip(".") for r in res]))[0][::-1]
            arxiv_id = re.sub(r'v([0-9])', '', arxiv_id)
            identifier['arXiv'] = arxiv_id
        else:
            identifier['None'] = ""
    return identifier


def get_metadata(user_id, stream):
    identifier = get_identifier(stream)
    (key, value), = identifier.items()
    if key == 'doi':
        print("doi")
    elif key == 'arXiv':
        print("arXiv")
    else:
        sleep(1)
    return 1
