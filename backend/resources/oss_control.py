from backend.models.db_models import API
from flask_restful import reqparse
import werkzeug.datastructures
from flask import Flask, json, request, make_response, jsonify
from backend.utils.oss import auth, bucket
from backend.handlers.DocHandler import upload


class UploadDocuments(API):
    """
    上传到oss存储
    """

    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('data', type=werkzeug.datastructures.FileStorage, location='files')
        args = parse.parse_args()
        stream = args['data'].stream
        upload(stream=stream, user_id='5cf0c31890f43a4e53492b34', user_name='testname')
        return "helloworld"
