import pymongo
import os, sys
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

def authenticate(username, password):
    user_taken = is_user_taken(username, username)
    if not user_taken:
        return False
    
    elif user_taken == 'Username Taken':
        u = 'username'

    elif user_taken == 'Email Taken':
        u = 'email'
        
    user = collection.find_one({ u: username })

    if password == encryption.decrypt(user['password']):
        return user
    
    return False
    

def create_user(username, first_name, last_name, email, age, password1, password2):
    minimum_age = settings.Rules["MINIMUM_AGE"]
    user_taken = is_user_taken(username, email)

    if not(age < minimum_age or user_taken or password1 != password2):
        collection.insert_one({
            "username": username,
            "first_name":first_name,
            "last_name":last_name,
            "email":email.lower(),
            "age":age,
            "password": encryption.encrypt(password1),
            "email_confirmed": False
        })
        if collection.find_one({'username':username}):
            return 'User created successfully!'
        else:
            return settings.Syntax["UNKNOWN_ERROR_TRY_AGAIN"]

    elif age < minimum_age:
        return "Users must be at least 13 years of age"

    elif user_taken:
        return user_taken

    elif password1 != password2:
        return "Your passwords must match"
    
    elif '@' in username:
        return "username cannot contain an @ symbol"

    else:
        return settings.Syntax["UNKNOWN_ERROR_TRY_AGAIN"]