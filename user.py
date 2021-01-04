import datetime
import smtplib
import os

import blueprints.posts.post_database                      as pdb
import blueprints.follow.follow_database                   as fdb
import blueprints.email_verification.verification_database as vdb

class User:
    def __init__(self, id, username, first_name, last_name, email):
        self.id                  = id
        self.username            = username
        self.first_name          = first_name
        self.last_name           = last_name
        self.email               = email
        self.fullname            = self.first_name + ' ' + self.last_name
        self.email_confirmed     = vdb.email_confirmed(self)
        self.posts               = pdb.get_posts(self.id)
        self.number_of_followers = fdb.count_followers(self.id)

    def time_since_post(self, time_posted, current_time = int(datetime.datetime.now().timestamp())):
        seconds_since_posted = current_time - time_posted
        days_since_posted    = int(seconds_since_posted/86400)
        hours_since_posted   = int(seconds_since_posted/3600)
        minutes_since_posted = int(seconds_since_posted/60)

        if days_since_posted:
            return f"{days_since_posted} days"

        elif hours_since_posted:
            return f"{hours_since_posted} hours"

        elif minutes_since_posted > 1:
            return f"{minutes_since_posted} minutes"

        elif minutes_since_posted == 1:
            return f"{minutes_since_posted} minute"

        else:
            print('s', seconds_since_posted)
            return "less than a minute"

    def send_verification_email(self):        
        SLAKR_EMAIL_ADDRESS  = os.environ.get('slakremail')
        SLAKR_EMAIL_PASSWORD = os.environ.get('slakremailpassword')
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()

            smtp.login(
                SLAKR_EMAIL_ADDRESS,
                SLAKR_EMAIL_PASSWORD
            )

            subject = 'Chatre Email Verification'
            body    = f'Verification Code:\n{vf()}'

            msg     = f'Subject: {subject}\n\n{body}'
            
            smtp.sendmail(SLAKR_EMAIL_ADDRESS, self.email, msg)
