import datetime

class User:
    def __init__(self, id, username, first_name, last_name, email, posts):
        self.id              = id
        self.username        = username
        self.first_name      = first_name
        self.last_name       = last_name
        self.email           = email
        self.fullname        = self.first_name + ' ' + self.last_name
        self.email_confirmed = False
        self.posts           = posts

    def time_since_post(self, time_posted, current_time = int(datetime.datetime.now().timestamp())):
        #print((float(timestamp1)-float(timestamp2))/(60*60*24))
        time_since_posted = current_time - time_posted
        return int(time_since_posted/86400)