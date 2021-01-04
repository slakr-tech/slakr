import pymongo
import random
import os, sys
from bson.objectid import ObjectId
sys.path.append('../..')
import encryption as enc
from datetime import datetime as dt

connectionUri = os.environ.get('chatreMongoConnectionUri')
cluster = pymongo.MongoClient(connectionUri)
db = cluster["users"]
verification_collection = db["verification"]

def generate_code(length=6):
    return "".join([str(random.randint(0,9)) for _ in range(length)])

def change_code(u):
    verification_collection.update({"_id":u.id},{
        "$set": {
            "code": generate_code()
        }}
    )

def date_difference_too_much(u, too_much_time=86400):
    verification_code_doc = verification_collection.find_one({
        "_id":u.id
    })
    now = int(dt.now().timestamp())
    if verification_code_doc['time_code_generated'] - too_much_time > now:
        change_code(u)

def get_verification_code(u):
    verification_code_doc_exists = verification_collection.count_documents({
        "_id":u.id
    })

    if verification_code_doc_exists:
        date_difference_too_much(u)
        verification_code_doc = verification_collection.find_one({
            "_id":u.id
        })
        return verification_code_doc['code']
    
    else:
        code = generate_code()
        verification_collection.insert_one({
            "_id": u.id,
            "code": code,
            "confirmed": False,
            "time_code_generated":int(dt.now().timestamp())
        })

        return code

def confirm(u):
    verification_collection.update({"_id":u.id},{
        "$set": {
            "confirmed": True
        }}
    )

def email_confirmed(u):
    if bool(verification_collection.count_documents({"_id":u.id})):
        verification_code_doc = verification_collection.find_one({
            "_id":u.id
        })

        return verification_code_doc['confirmed']

    else:
        return False

def test():
    print(generate_code())

if __name__ == '__main__':
    test()