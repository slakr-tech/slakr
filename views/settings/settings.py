from flask import Blueprint, render_template, session, redirect, url_for, request
import sys
sys.path.append('../..')

settings = Blueprint("settings", __name__, static_folder='static', template_folder='templates')

@settings.route('/')
def settings_page():
    return render_template('settings.html')