from flask import Flask, render_template, request, redirect, url_for, flash, session
import database

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/signin')
def signin():
    return "This page has not been created yet"

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "GET":
        return render_template('signup.html')
    
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