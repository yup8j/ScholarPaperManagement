from mongoengine import connect
from backend.models.db_models import *

def register_database(app):
    database = app.config['MONGODB_DB']
    connect(database)