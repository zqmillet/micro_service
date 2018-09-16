from utilities.mongo import MongoCollection

class MongoDatabase:
    __database = None
    __session = None

    def __init__(self, database, session):
        self.__database = database
        self.__session = session

    def fetch_collection_name_list(self):
        return self.__database.collection_names()

    def fetch_collection(self, collection_name):
        return MongoCollection(self.__database[collection_name])

    def __getitem__(self, collection_name):
        return self.fetch_collection(collection_name)

    def drop(self):
        self.__session.drop_database(self.__database.name)
