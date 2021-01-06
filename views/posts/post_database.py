import pymongo
from bson.objectid import ObjectId
import os, sys
sys.path.append('../..')
import app_settings
import encryption as enc
import user_database as db
import re
from datetime import datetime, timedelta

connectionUri = os.environ.get('chatreMongoConnectionUri')
cluster = pymongo.MongoClient(connectionUri)
database = cluster["users"]
post_collection = database["posts"]

def get_posts(user_id):
    print('get_posts called')
    post_documents = post_collection.find({"user_id": user_id})
    posts = []
    for post in post_documents:
        posts.append(post)
    return posts

def get_posts_by_multiple_users(user_ids):
    # { field: { $in: [<value1>, <value2>, ... <valueN> ] } }
    post_documents = post_collection.find({"user_id": {
        "$in" : user_ids
    }}).sort('date')

    posts = []
    for post in post_documents:
        posts.append(post)
    return posts

def add_post(post, post_title, user_id):
    date = datetime.now().timestamp()
    post_collection.insert_one({
        "user_id":user_id,
        "username":db.get_user(user_id, "_id").username,
        "title":post_title,
        "content":post,
        "date":int(date)
    })

def remove_post(user_id, post_id):
    post = {"_id":ObjectId(post_id), "user_id":user_id}
    post_collection.delete_one(post)

def post_exists(user_id, post_id):
    post = post_collection.find_one({"_id":ObjectId(post_id), "user_id":user_id})

    if post:
        return True
    return False
