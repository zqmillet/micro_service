from utilities.mongo import MongoItem

class MongoCollection:
    __collection = None

    def __init__(self, collection):
        self.__collection = collection

    def __iter__(self):
        for item in self.find({}):
            yield MongoItem(item, self.__collection)

    def find(self, condition = {}):
        return self.__collection.find(condition)

    def insert(self, data):
        self.__collection.insert_one(data)

    def clear_items(self):
        self.__collection.remove()

    def drop(self):
        self.__collection.drop()
