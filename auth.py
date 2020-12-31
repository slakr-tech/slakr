from flask import session
from user import User
import database as db
import settings

def auth():
    if session.get("USERNAME") and session.get("PASSWORD"):
        auth = db.authenticate(session["USERNAME"], session["PASSWORD"])
        signed_in = bool(auth)
        user = ''
        
        if signed_in:
            user = User(auth['_id'], auth['username'], auth['first_name'], auth['last_name'], auth['email'], auth['posts'])
            print(settings.Syntax['SEP'])
            print(str(auth['_id']))
            print(settings.Syntax['SEP'])
        
        return [signed_in, user]
    return [False, '']
