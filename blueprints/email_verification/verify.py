from flask import Blueprint, render_template, session, redirect, url_for, request, flash
import sys,os
import smtplib
sys.path.append('../..')
from auth import auth
import app_settings
import blueprints.email_verification.verification_database as vdb

verify = Blueprint("verify", __name__, static_folder='static', template_folder='templates')

def send_verification_email(u):
    SLAKR_EMAIL_ADDRESS  = os.environ.get('slakremail')
    SLAKR_EMAIL_PASSWORD = os.environ.get('slakremailpassword')

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        print(type(SLAKR_EMAIL_ADDRESS))
        print(type(SLAKR_EMAIL_PASSWORD))

        smtp.login(
            SLAKR_EMAIL_ADDRESS,
            SLAKR_EMAIL_PASSWORD
        )
        print(2)
        subject = 'Chatre Email Verification'
        body    = f'Verification Code:\n{ vdb.get_verification_code(u) }'

        msg     = f'Subject: {subject}\n\n{body}'
        
        app_settings.debug('send email: ' + u.email)
        smtp.sendmail(SLAKR_EMAIL_ADDRESS, u.email, msg)

@verify.route('/', methods=['GET', 'POST'])
def verification():
    auth_status = auth()
    if request.method == 'GET':
        if auth_status[1].email_confirmed:
            flash('Email is already confirmed')
            return redirect(url_for('index'))
        app_settings.debug('verification: ' + auth_status[1].email)
        send_verification_email(auth_status[1])
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