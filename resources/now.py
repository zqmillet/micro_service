import datetime

class Now:
    __time = None

    def __init__(self):
        self.__time = datetime.datetime.today()

    def update(self):
        self.__time = datetime.datetime.today()

    def __str__(self):
        return str(self.__time)

now = Now()
