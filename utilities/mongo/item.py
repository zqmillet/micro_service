class MongoItem:
    __item = None
    __Table = None

    def __init__(self, item, table):
        self.__item = item
        self.__table = table

    def __getitem__(self, key):
        return self.__item.get(key, None)

    def __setitem__(self, key, value):
        self.__table.update({
            '_id': self.__item['_id']
        }, {
            '$set': {
                key: value
            }
        }, upsert = False)
        self.__item[key] = value
