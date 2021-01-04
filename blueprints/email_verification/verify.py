from flask import Blueprint, render_template, session, redirect, url_for, request, flash
import sys,os
import smtplib
sys.path.append('../..')
from auth import auth
import app_settings
import blueprints.email_verification.verification_database as vdb

verify = Blueprint("verify", __name__, static_folder='static', template_folder='templates')

@verify.route('/', methods=['GET', 'POST'])
def verification():
    auth_status = auth()
    if request.method == 'GET':
        if auth_status[1].email_confirmed:
            flash('Email is already confirmed')
            return redirect(url_for('index'))
        app_settings.debug('verification: ' + auth_status[1].email)
        auth_status[1].send_verification_email()
        return render_template('verification.html', signed_in=auth_status[0], user=auth_status[1])

    elif request.method == 'POST':
        verification_code = vdb.get_verification_code(auth_status[1])
        if verification_code == request.form['code']:
            vdb.confirm(auth_status[1])
            flash('Email Verified')
            return redirect(url_for('index'))

        else:
            flash('Your verification code was incorrect')
            return redirect(url_for('verification'))