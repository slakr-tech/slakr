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
    follow = follow_collection.find({
        "follower":ObjectId(follower),
        "following":ObjectId(following)
    }).count()

    return follow

def get_followers(following, count=True):
    query = {"following":following}
    query_results = follow_collection.find(query)

    if count:
        return query_results.count()

    else:
        return query_results