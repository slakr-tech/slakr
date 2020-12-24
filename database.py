import pymongo
import os, sys
import errors
import settings
import encryption

connectionUri = os.environ.get('chatreMongoConnectionUri')
cluster = pymongo.MongoClient(connectionUri)
db = cluster["users"]
collection = db["users"]

def is_user_taken(username, email):
    if collection.find({ "username":username }).count():
        return 'Username Taken'
    
    elif collection.find({ 'email':email }).count():
        return 'Email Taken'

    else:
        return False


def create_user(username, first_name, last_name, email, age, password1, password2):
    try:
        minimum_age = settings.Rules["MINIMUM_AGE"]
        user_taken = is_user_taken(username, email)

        if age < minimum_age:
            raise errors.AgeError(age)
        
        elif user_taken:
            raise errors.UserTakenError(user_taken)

        elif password1 != password2:
            raise errors.PasswordsDoNotMatchError('Your passwords must match')

        collection.insert_one({
            "username": username,
            "first_name":first_name,
            "last_name":last_name,
            "email":email,
            "age":age,
            "password": encryption.encrypt(password1),
        })

        return 'User created successfully!'

    except:
        return sys.exc_info()[0]