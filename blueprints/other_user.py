from flask import Blueprint, render_template, session, redirect, url_for, request
import sys
sys.path.append("..")
import database as db
from auth import auth
import user

other_users = Blueprint("user", __name__, static_folder='static', template_folder='templates')

@other_users.route('/')
def general_user_page():
    return "User page"

@other_users.route('/profile/<username>')
def specific_user_page(username):
    auth_status = auth()
    other_user = db.get_user(username)
    
    if other_user:
        return render_template('other_user.html', signed_in=auth_status[0], user=auth_status[1], other_user=other_user)
    return "could not find page for: " + username

@other_users.route('/search')
def search():
    auth_status = auth()
    user_search = request.args.get('q')
    if user_search:
        results = db.search_users(user_search)
        return render_template('search.html', signed_in=auth_status[0], user=auth_status[1], results=results, user_search=user_search)
    
    else:
        return 'no results found'

# home page redirects
def index_page_redirect():
    return redirect(url_for('index'))

other_users.add_url_rule('/profile', 'index_page_redirect', index_page_redirect)

