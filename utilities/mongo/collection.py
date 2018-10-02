from utilities.mongo import MongoItem

class MongoCollection:
    '''
    this class is used to manage the collection of the mongo database.

    member veriables:
        - __collection <pymongo.collection.Collection>:
            this is the instance of the class pymongo.collection.Collection.
    '''

    __collection = None

    def __init__(self, collection):
        '''
        this is the constructor of the class MongoCollection.

        parameters:
            - collection <pymongo.collection.Collection>:
                this is the instance of the class pymongo.collection.Collection.

        return:
            nothing.
        '''

        self.__collection = collection

    def __iter__(self):
        '''
        override the function __iter__ of the class MongoCollection, so we can iterate its items by

        for item in mongo_collection:
            pass

        parameters:
            nothing.

        return:
            nothing.
        '''

        for item in self.find({}):
            yield MongoItem(item, self.__collection)

    def find(self, condition = {}):
        '''
        this function is used to provide the function find of the class pymongo.collection.Collection.

        parameters:
            - condition <dict>:
                the condition of query.

        return <pymongo.cursor.Cursor>:
            the cursor of the mongo.
        '''

        return self.__collection.find(condition)

    def insert(self, data):
        '''
        this function is used to insert a data into the MongoCollection.

        parameters:
            - data <dict>:
                the data.

        return:
            nothing.
        '''

        self.__collection.insert(data)

    def clear_items(self):
        '''
        this function is used to clear all items of the MongoCollection.

        parameters:
            nothing.

        return:
            nothing.
        '''

        self.__collection.remove()

    def drop(self):
        '''
        this function is used to drop the MongoCollection.

        parameters:
            nothing.

        return:
            nothing.
        '''

        self.__collection.drop()
