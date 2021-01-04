import pymongo
import random
import os, sys
from bson.objectid import ObjectId
sys.path.append('../..')
import encryption as enc
from datetime import datetime, timedelta

connectionUri = os.environ.get('chatreMongoConnectionUri')
cluster = pymongo.MongoClient(connectionUri)
db = cluster["users"]
verification_collection = db["verification"]

def generate_code(length=6):
    return "".join([str(random.randint(0,9)) for _ in range(length)])

def get_verification_code(u):
    verification_code_doc_exists = verification_collection.count_documents({
        "_id":u.id
    })

    if verification_code_doc_exists:
        verification_code_doc = verification_collection.find_one({
            "_id":u.id
        })
        return verification_code_doc['code']
    
    else:
        code = generate_code()
        verification_collection.insert_one({
            "_id": u.id,
            "code": code
        })

        return code

def email_confirmed(u):
    verification_code_doc_exists = verification_collection.count_documents({
        "_id":u.id
    })

    return bool(verification_code_doc_exists)

def test():
    print(generate_code())

if __name__ == '__main__':
    test()