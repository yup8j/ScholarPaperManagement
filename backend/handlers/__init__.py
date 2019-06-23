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
from pdfminer import pdfparser, pdfdocument, pdftypes, converter
from backend.utils.oss import *
import requests
import json
from concurrent.futures import ThreadPoolExecutor
from backend.models.db_models import Documents, Topic
from backend.models.db_models import Metadata, User
