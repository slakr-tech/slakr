from flask import Blueprint, render_template

users = Blueprint("user", __name__, static_folder='static', template_folder='templates')

@users.route('/')
def userPage():
    return "User page"