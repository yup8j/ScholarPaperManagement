from pymongo import MongoClient
from flask import Flask
from flask_pymongo import PyMongo
import datetime
# client = MongoClient(
#     'mongodb://root:qwerty2019()-=@dds-wz9f23f0cffe4b341504-pub.mongodb.rds.aliyuncs.com:3717,dds-wz9f23f0cffe4b342338-pub.mongodb.rds.aliyuncs.com:3717/admin?replicaSet=mgset-15064123')
#
# db = client.test_shi
# collection = db.shi_test1
#
# post = {"author": "Maxsu",
#          "text": "My first blog post!",
#          "tags": ["mongodb", "python", "pymongo"],
#          "date": datetime.datetime.utcnow()}
#
# posts = db.posts
# post_id = posts.insert_one(post).inserted_id
# print ("post id is ", post_id)

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://root:qwerty2019()-=@dds-wz9f23f0cffe4b341504-pub.mongodb.rds.aliyuncs.com:3717,dds-wz9f23f0cffe4b342338-pub.mongodb.rds.aliyuncs.com:3717/test_shi?authSource=admin"
mongo = PyMongo(app)

@app.route("/")
def home_page():
    online_users = mongo.db.posts.find_one_or_404({"author": "Maxsu"})
    print(online_users)
    return "hello_world"

if __name__ == "__main__":
    app.run(debug=True)