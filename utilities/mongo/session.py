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
        # if not database_name in self.fetch_database_name_list():
        #     return None

        return MongoDatabase(self.__client[database_name])

    def iterate_item(self, database_name, table_name):
        # mongo_database = self.fetch_database(database_name)
        # if mongo_database is None:
        #     return

        # mongo_table = mongo_database.fetch_table(table_name)
        # if mongo_table is None:
        #     return

        for item in mongo_table:
            yield item

    def __getitem__(self, database_name):
        return self.fetch_database(database_name)

def testcases():
    mongo_session = MongoSession(
        host = 'localhost',
        port = 27017,
        username = 'admin',
        password = 'admin'
    )

    for item in mongo_session.iterate_item(database_name = 'adin', table_name = 'test'):
        print(item)

    mongo_database = mongo_session['adin']
    mongo_table = mongo_database['test123']
    mongo_table.insert({'abc': 'jdfskjfksd'})

if __name__ == '__main__':
    testcases()
