import json

class MongoItem:
    __item = None
    __Table = None

    __ID = '_id'

    def __init__(self, item, table):
        self.__item = item
        self.__table = table

    def __getitem__(self, key):
        return self.__item.get(key, None)

    def __setitem__(self, key, value):
        self.__table.update({
            self.__ID: self.__item[self.__ID]
        }, {
            '$set': {
                key: value
            }
        }, upsert = False)
        self.__item[key] = value

    def __str__(self):
        dictionary = {key: value for key, value in self.__item.items() if not key == self.__ID}
        return str(self.__item[self.__ID]) + ': ' + json.dumps(dictionary, ensure_ascii = False)
