from flask import Blueprint, render_template, session, redirect, url_for, request, flash
import sys
sys.path.append("../..")
import user_database as db
import blueprints.posts.post_database as pdb
from auth import auth
from user import User
import app_settings

posts = Blueprint("posts", __name__, static_folder='static', template_folder='templates')

@posts.route('/create')
def create_post():
    auth_status = auth()
    post       = request.args.get('p')
    post_title = request.args.get('t')
    print('auth status 1:', auth_status[1].id)
    for i in auth_status:
        print(auth_status)
    if post and auth_status[0]:
        if not post_title:
            post_title = 'Post'
        pdb.add_post(post, post_title, auth_status[1].id)
        flash('post created')

    elif not post:
        flash('You must write something for your post')

    elif not auth_status[0]:
        flash('You must be signed in to create a post, make sure you have cookies enabled')

    return redirect(url_for('myprofile'))

@posts.route('/remove')
def delete_post():
    auth_status = auth()
    post_id = request.args.get('p')
    print(pdb.post_exists(auth_status[1].id, post_id))
    if post_id:
        pdb.remove_post(auth_status[1].id, post_id)
        flash('post removed')

    elif not post_id:
        flash('Could not delete post')

    elif not auth_status[0]:
        flash('You must be signed in to delete a post, make sure you have cookies enabled')

    return redirect(url_for('index'))