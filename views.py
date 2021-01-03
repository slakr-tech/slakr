from flask import Flask, render_template, request, redirect, url_for, flash, session
import feed
import user_database as db
import encryption as enc
import app_settings
from auth import auth

# BLUEPRINTS
from blueprints.other_users.other_user import other_users
from blueprints.posts.posts import posts
from blueprints.follow.follow import follow
from blueprints.settings.settings import settings

app = Flask(__name__)
app.register_blueprint(other_users, url_prefix="/users")
app.register_blueprint(posts, url_prefix="/post")
app.register_blueprint(follow, url_prefix="/follow")
app.register_blueprint(settings, url_prefix="/settings")

@app.route('/')
def index():
    auth_status = auth()
    if auth_status[0]:
        return render_template("index.html", signed_in=auth_status[0],
        user=auth_status[1], feed=feed.get_feed(auth_status[1].id))
    
    else:
        return render_template("index.html", signed_in=auth_status[0])

@app.route('/myprofile')
def myprofile():
    auth_status = auth()
    return render_template("post.html", signed_in=auth_status[0],user=auth_status[1])


@app.route('/signin', methods=["GET", "POST"])
def signin():
    auth_status = auth()
    if request.method == "GET":
        if not auth_status[0]:
            return render_template('login.html', signed_in=auth_status[0], user=auth_status[1])
        else:
            return redirect(url_for('index'))
    
    if request.method == "POST":
        if db.authenticate(request.form["un"], request.form["pw"]):
            if request.form.get('session'):
                session["USERNAME"] = request.form["un"]
                session["PASSWORD"] = request.form["pw"]
            
            else:
                flash('You must check \"keep me logged in\" to sign in')
                return redirect(url_for('signin'))

            flash("successfully logged in")
        else:
            flash("wrong username or password")
            return redirect(url_for('signin'))
        return redirect(url_for('signin'))
    

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    auth_status = auth()
    if request.method == "GET":
        if not auth_status[0]:
            return render_template('signup.html', signed_in=auth_status[0], user=auth_status[1])
        else:
            return redirect(url_for('signup'))
    
    elif request.method == "POST":
        fn = request.form["fn"]
        ln = request.form["ln"]
        age = int(request.form["age"])
        email = request.form["email"]
        username = request.form["uname"]
        password1 = request.form["pw"]
        password2 = request.form["pwc"]

        
        create_user = db.create_user(username,fn,ln,email,age,password1,password2)
        flash(create_user)
        return redirect(url_for('index'))

@app.route('/signout')
def signout():
    session.pop('USERNAME', None)
    session.pop('PASSWORD', None)
    return redirect(url_for('index'))