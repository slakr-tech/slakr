class AgeError(Exception):
    def __init__(self, age, message):
        self.age = age
        self.message = message
        super().__init__(self.message)