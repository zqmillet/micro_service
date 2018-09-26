from exceptions import BaseException

class TypeError(BaseException):
    type = None
    message = 'unexcepted type {type}.'

    def __init__(self, type):
        self.type = type
