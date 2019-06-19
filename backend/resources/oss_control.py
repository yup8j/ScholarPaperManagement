from backend.resources import *


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
    # TODO：完善lib相关部分的删除
    def post(self):
        request.get_json(force=True)
        parse = reqparse.RequestParser()
        parse.add_argument('document_id', type=str)
        args = parse.parse_args()
        document_id = args['document_id']
        print(document_id)
        self.response = make_response()
        try:
            delete_document(document_id=document_id, user_id='5cf0c31890f43a4e53492b34')
            self.response.status_code = 200
        except Exception as e:
            print(str(e))
            self.response.status_code = 403
        return self.response
