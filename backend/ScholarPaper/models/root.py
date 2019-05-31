from .required_modules import *
from flask import jsonify


class Main(API):
    def __init__(self, db):
        super(Main, self).__init__(db)

    def get(self):
        data = self.db
        if data == None:
            print("Data is None!")
            return jsonify({})
        else:
            result = [x.username for x in list(data)]
            return jsonify(dict(enumerate(result)))

    def post(self):
        # code here
        return 0
