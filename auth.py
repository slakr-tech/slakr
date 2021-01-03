from flask import session
from user import User
import user_database as db
import app_settings

def auth():
    if session.get("USERNAME") and session.get("PASSWORD"):
        auth = db.authenticate(session["USERNAME"], session["PASSWORD"])
        signed_in = bool(auth)
        user = ''
        
        if signed_in:
            user = User(auth['_id'], auth['username'], auth['first_name'], auth['last_name'], auth['email'])
        
        return [signed_in, user]
    return [False, {}]
