import yagmail
from random import randint
import os

class User:
    def __init__(self, username, first_name, last_name, email, email_confirmed):
        self.username        = username
        self.first_name      = first_name
        self.last_name       = last_name
        self.email           = email
        self.email_confirmed = email_confirmed

    def send_confirmation_email(self):
        yagmail.register(os.environ["chatreEmail"], os.environ["chatreEmailPassword"])
        yag = yagmail.SMTP(os.environ["chatreEmail"])
        with open('email.html', 'r') as f:
            email_content = f.read()
        yag.send(to = self.email,
            subject = 'CHATRE email verification',
            contents = email_content.format(
                self.first_name,
                self.email,
                randint(100000, 999999)
                )
            )
