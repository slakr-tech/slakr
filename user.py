import datetime

import blueprints.posts.post_database    as pdb
import blueprints.follow.follow_database as fdb

class User:
    def __init__(self, id, username, first_name, last_name, email):
        self.id                  = id
        self.username            = username
        self.first_name          = first_name
        self.last_name           = last_name
        self.email               = email
        self.fullname            = self.first_name + ' ' + self.last_name
        self.email_confirmed     = False
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

    def verify_email(self):
        pass