from backend.models.db_models import API
from flask_restful import reqparse
import werkzeug.datastructures
from flask import Flask, json, request, make_response, jsonify, send_file
from backend.utils.oss import auth, bucket
from backend.handlers.DocHandler import upload, download, delete_document
import io
from flask import Flask, json, request, make_response, jsonify
from flask_restful import Resource
from backend.handlers import LoginHandler
from backend.models.db_models import API
from flask_jwt_extended import jwt_required, get_jwt_identity