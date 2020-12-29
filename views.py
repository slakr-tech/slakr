from flask import Flask, render_template, request, redirect, url_for, flash, session
from user import User
import database
import encryption
import settings

app = Flask(__name__)

def auth():
    if session.get("USERNAME") and session.get("PASSWORD"):
        auth = database.authenticate(session["USERNAME"], session["PASSWORD"])
        signed_in = bool(auth)
        user = ''
        
        if signed_in:
            user = User(auth['_id'], auth['username'], auth['first_name'], auth['last_name'], auth['email'])
            print(settings.Syntax['SEP'])
            print(str(auth['_id']))
            print(settings.Syntax['SEP'])
        
        return [signed_in, user]
    return [False, '']

@app.route('/')
def index():
    auth_status = auth()
    print(auth_status)
    return render_template("index.html", signed_in=auth_status[0], user=auth_status[1])


@app.route('/signin', methods=["GET", "POST"])
def signin():
    auth_status = auth()
    if request.method == "GET":
        if not auth_status[0]:
            return render_template('login.html', signed_in=auth_status[0], user=auth_status[1])
        else:
            return redirect(url_for('index'))
    
    if request.method == "POST":
        if database.authenticate(request.form["un"], request.form["pw"]):
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

        
        create_user = database.create_user(username,fn,ln,email,age,password1,password2)
        flash(create_user)
        return redirect(url_for('index'))

@app.route('/signout')
def signout():
    session.pop('USERNAME', None)
    session.pop('PASSWORD', None)
    return redirect(url_for('index'))