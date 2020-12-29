from flask import Blueprint, render_template, session
import sys
sys.path.append("..")
import database
from auth import auth
import user

other_users = Blueprint("user", __name__, static_folder='static', template_folder='templates')

@other_users.route('/')
def general_user_page():
    return "User page"

@other_users.route('/<username>')
def specific_user_page(username):
    auth_status = auth()
    other_user = database.get_user(username)
    
    if other_user:
        return render_template('other_user.html', signed_in=auth_status[0], user=auth_status[1], other_user=other_user)
    return "could not find page for: " + username