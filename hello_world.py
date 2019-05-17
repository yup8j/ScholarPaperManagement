import requests
from get_paper_id import get_identifier
import json

pdf_list = [r'1805.03977.pdf', r'osdi16-abadi.pdf', r'1905.06316.pdf', r'2016 Isaure Chauvot de Beauchene.pdf',
            r'1-s2.0-S136403211630288X-main.pdf']


def make_ssapi_request(pdf_id):
    url = "http://api.semanticscholar.org/v1/paper/"
    final = "?include_unknown_references=TRUE"
    (key, value), = pdf_id.items()
    if key == 'arXiv':
        url = url + "arXiv:" + value + final
    elif key == 'doi':
        url = url + value + final
    else:
        url = ""
        return url
    if url:
        response = requests.get(url=url)
        json_data = json.loads(response.text)
        return json_data


for i in pdf_list:
    pdf_id = get_identifier(i)
    data = make_ssapi_request(pdf_id=pdf_id)
    if data:
        try:
            au = data['authors']
            print(au)
        except KeyError:
            print("No authors data")
