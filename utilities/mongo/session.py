import pymongo

from utilities.mongo import MongoDatabase
from exceptions import ConnectionRefusedError, ConnectionTimeOut, AuthenticationError

class MongoSession:
    __client = None
    __database_type = 'mongo'
    __exception_eigen_dictionary = {
        'connection refused':    ConnectionRefusedError,
        'timed out':             ConnectionTimeOut,
        'authentication failed': AuthenticationError
    }

    def __init__(self, host, port, username, password, timeout = 1000, maximum_retries = 10):
        for _ in range(maximum_retries):
            try:
                self.__client = pymongo.MongoClient(
                    'mongodb://{username}:{password}@{host}:{port}'.format(
                        host     = host,
                        port     = port,
                        username = username,
                        password = password
                    ),
                    connectTimeoutMS = timeout
                )
            except Exception as e:
                for eigen, exception in self.__exception_eigen_dictionary.items():
                    if eigen in str(e).lower():
                        raise exception(database_type = self.__database_type, host = host, port = port)
                else:
                    print(e)

    def fetch_database_name_list(self):
        return self.__client.database_names()

    def fetch_database(self, database_name):
        return MongoDatabase(self.__client[database_name], self)

    def drop_database(self, database_name):
        self.__client.drop_database(database_name)

    def __getitem__(self, database_name):
        return self.fetch_database(database_name)
