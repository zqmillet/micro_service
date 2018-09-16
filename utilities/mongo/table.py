from utilities.mongo import MongoItem

class MongoTable:
    __table = None

    def __init__(self, table):
        self.__table = table

    def __iter__(self):
        for item in self.find({}):
            yield MongoItem(item, self.__table)

    def find(self, condition = {}):
        return self.__table.find(condition)
