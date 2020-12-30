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