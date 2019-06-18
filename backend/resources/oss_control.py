from backend.models.db_models import API
from flask_restful import reqparse
import werkzeug.datastructures
from flask import Flask, json, request, make_response, jsonify, send_file
from backend.utils.oss import auth, bucket
from backend.handlers.DocHandler import upload, download, delete_document
import io


class UploadDocuments(API):
    """
    上传到oss存储
    """

    def post(self):
        parse = reqparse.RequestParser()
        self.response = make_response()
        parse.add_argument('data', type=werkzeug.datastructures.FileStorage, location='files')
        args = parse.parse_args()
        stream = args['data'].stream
        j, c = upload(stream=stream, user_id='5cf0c31890f43a4e53492b34', user_name='testname')
        self.response.status_code = c
        if c == 200:
            self.response = jsonify(j)
        return self.response


class DownloadDocuments(API):
    """
    下载文献
    """

    def get(self, document_id):
        doc_name, doc_stream = download(document_id, user_id='5cf0c31890f43a4e53492b34')
        # response = make_response(doc_stream)
        # response.headers.set('Content-Type', 'application/pdf')
        # return response
        return send_file(
            io.BytesIO(doc_stream.read()),
            mimetype='application/pdf',
            as_attachment=True,
            attachment_filename='%s.pdf' % doc_name)


class DeleteDocuments(API):
    """
    彻底删除文献
    """

    def post(self, document_id):
        delete_document(document_id=document_id, user_id='5cf0c31890f43a4e53492b34')
        return "helloworld"

# class GetNote(API):
#     """
#     如果有，则取回，如果没有，则新建
#     """
