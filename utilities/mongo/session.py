import pymongo

from utilities.mongo import MongoDatabase

class MongoSession:
    __client = None

    def __init__(self, host, port, username, password):
        self.__client = pymongo.MongoClient(
            'mongodb://{username}:{password}@{host}:{port}'.format(
                host     = host,
                port     = port,
                username = username,
                password = password
            )
        )

    def fetch_database_name_list(self):
        return self.__client.database_names()

    def fetch_database(self, database_name):
        return MongoDatabase(self.__client[database_name], self)

    def iterate_item(self, database_name, collection_name):
        for item in self[database_name][collection_name]:
            yield item

    def drop_database(self, database_name):
        self.__client.drop_database(database_name)

    def __getitem__(self, database_name):
        return self.fetch_database(database_name)
