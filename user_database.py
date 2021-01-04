import pymongo
import os, sys
import app_settings
import encryption as enc
import re
from user import User
from datetime import datetime, timedelta

connectionUri = os.environ.get('chatreMongoConnectionUri')
cluster = pymongo.MongoClient(connectionUri)
db = cluster["users"]
user_collection = db["users"]

def is_user_taken(username, email):
    if user_collection.find({ "username":username }).count():
        return 'Username Taken'
    
    elif user_collection.find({ 'email':email }).count():
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

    user = user_collection.find_one({ u: username })

    if password == enc.decrypt(user['password']):
        return user
    
    return False
    

def create_user(username, first_name, last_name, email, age, password1, password2):
    not_allowed_chars = '[@_!#$%^&*()<>?/\|}]{~:,;+'
    # Rules
    age_rule = age < app_settings.Rules["MINIMUM_AGE"]
    user_taken = is_user_taken(username, email)
    password_match_rule = password1 != password2
    space_in_username_rule = ' ' in username
    special_char_in_username_rule = re.compile(not_allowed_chars).search(username)


    if not(age_rule or user_taken or password_match_rule or space_in_username_rule or special_char_in_username_rule):
        user_collection.insert_one({
            "username": username,
            "first_name":first_name,
            "last_name":last_name,
            "email":email.lower(),
            "age":age,
            "password": enc.encrypt(password1),
            "email_confirmed": False
        })
        if user_collection.find_one({'username':username}):
            return 'User created successfully! Please Sign in to your newly created chatre account!'
        else:
            return app_settings.Syntax["UNKNOWN_ERROR_TRY_AGAIN"]

    elif age_rule:
        return "Users must be at least 13 years of age"

    elif user_taken:
        return user_taken

    elif password_match_rule:
        return "Your passwords must match"

    elif space_in_username_rule:
        return "Username cannot contain a space in it"

    elif special_char_in_username_rule:
        return f"You cannot use any of the following characters in your username: {', '.join(not_allowed_chars)}"

    else:
        return app_settings.Syntax["UNKNOWN_ERROR_TRY_AGAIN"]

def get_user(username, get_by="username"):
    user = user_collection.find_one({get_by:username})
    if user:
        return User(user['_id'], user['username'], user['first_name'], user['last_name'], user['email'])
    else:
        return False

def search_users(search, search_by="username"):
    query = { search_by: { "$regex":search } }
    search_results = user_collection.find(query)
    results = []
    for result in search_results:
        results.append(User(result['_id'], result['username'], result['first_name'], result['last_name'], result['email']))

    return results
