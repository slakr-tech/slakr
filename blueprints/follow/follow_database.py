import pymongo
import os, sys
from bson.objectid import ObjectId
import settings
import re
from user import User
from datetime import datetime, timedelta

connectionUri = os.environ.get('chatreMongoConnectionUri')
cluster = pymongo.MongoClient(connectionUri)
db = cluster["users"]
follow_collection = db["follow"]

def follow(follower, following):
    follow_collection.insert_one({
        "follower":ObjectId(follower),
        "following":ObjectId(following)
    })

def unfollow(follower, following):
    follow_collection.delete_one({
        "follower":ObjectId(follower),
        "following":ObjectId(following)
    })

def is_following(follower, following):
    print('\nis following:')
    print(follower)
    print(following)
    print(type(follower))
    print(type(following))
    follow = follow_collection.find({
        "follower":ObjectId(follower),
        "following":ObjectId(following)
    }).count()

    return follow