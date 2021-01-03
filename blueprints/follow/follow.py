from flask import Blueprint, render_template, session, redirect, url_for, request
import sys
sys.path.append("../..")
import blueprints.follow.follow_database as fdb
from auth import auth

follow = Blueprint("follow", __name__, static_folder='static', template_folder='templates')

@follow.route('/follow')
def follow_user():
    fdb.follow(auth()[1].id, request.args['following'])
    return redirect(url_for('other_user.specific_user_page', username=request.args.get('user')))

@follow.route('/unfollow')
def unfollow_user():
    fdb.unfollow(auth()[1].id, request.args['following'])
    return redirect(url_for('other_user.specific_user_page', username=request.args.get('user')))

