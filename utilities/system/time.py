import datetime

class Time:
    __now = None

    def __init__(self):
        self.__now = datetime.datetime.today()

    def __str__(self):
        return str(self.__now)

    def update(self):
        self.__now = datetime.datetime.today()
