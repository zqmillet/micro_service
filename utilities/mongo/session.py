import pymongo

from utilities.mongo import MongoDatabase
from exceptions import ConnectionRefusedError, ConnectionTimeOut, AuthenticationError

class MongoSession:
    __client = None

    def __init__(self, host, port, username, password):
        # self.__client = pymongo.MongoClient(
        #     'mongodb://{username}:{password}@{host}:{port}'.format(
        #         host     = host,
        #         port     = port,
        #         username = username,
        #         password = password
        #     )
        # )
        try:
            self.__client = pymongo.MongoClient(
                'mongodb://{username}:{password}@{host}:{port}'.format(
                    host     = host,
                    port     = port,
                    username = username,
                    password = password
                )
            )
        except pymongo.errors.ConnectionFailure as e:
            if 'Connection refused' in str(e):
                raise ConnectionRefusedError(database_type = 'mongo', host = host, port = port)
            elif 'timed out' in str(e):
                raise ConnectionTimeOut(database_type = 'mongo', host = host, port = port)
        except pymongo.errors.ConfigurationError as e:
            if 'Authentication failed' in str(e):
                raise AuthenticationError(database_type = 'mongo', host = host, port = port)

    def fetch_database_name_list(self):
        return self.__client.database_names()

    def fetch_database(self, database_name):
        return MongoDatabase(self.__client[database_name], self)

    def drop_database(self, database_name):
        self.__client.drop_database(database_name)

    def __getitem__(self, database_name):
        return self.fetch_database(database_name)
