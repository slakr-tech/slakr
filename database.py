import pymongo
import os, sys
import settings
import encryption
import re

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
    not_allowed_chars = '[@_!#$%^&*()<>?/\|}]{~:,;+'
    # Rules
    age_rule = age < settings.Rules["MINIMUM_AGE"]
    user_taken = is_user_taken(username, email)
    password_match_rule = password1 != password2
    space_in_username_rule = ' ' in username
    special_char_in_username_rule = re.compile(not_allowed_chars).search(username)


    if not(age_rule or user_taken or password_match_rule or space_in_username_rule or special_char_in_username_rule):
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
        return settings.Syntax["UNKNOWN_ERROR_TRY_AGAIN"]