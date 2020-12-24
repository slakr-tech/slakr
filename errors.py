import settings

class AgeError(Exception):
    def __init__(self, age):
        self.age = age
        self.msg = f'User is only {self.age}. User must be at least {settings.Rules["MINIMUM_AGE"]}'
        super().__init__(self.msg)

class UserTakenError(Exception):
    def __init__(self, msg):
        self.msg = msg
        super().__init__(self.msg)

class PasswordsDoNotMatchError(Exception):
    def __init__(self, msg):
        self.msg = msg
        super().__init__(self.msg)