class SessionException(Exception):
    message:str

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

class ReleaseZero(SessionException):
    pass