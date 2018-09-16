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

def testcases():
    # create a mongo database session.
    mongo_session = MongoSession(
        host = 'localhost',
        port = 27017,
        username = 'admin',
        password = 'admin'
    )

    # create a new database, and create a new collection, then insert 10 items
    # into the new collection.
    for index in range(10):
        mongo_session['new_database']['new_collection'].insert(
            {
                'index': index,
                'name': 'test item {index}'.format(index = index)
            }
        )

    # print the new items.
    for item in mongo_session.iterate_item(database_name = 'new_database', collection_name = 'new_collection'):
        print(item)

    # change the name of the new items, and add new property for each item.
    for index, item in enumerate(mongo_session.iterate_item(database_name = 'new_database', collection_name = 'new_collection')):
        item['name'] = 'item {index}'.format(index = index)
        item['height'] = index

    # print the new items.
    for item in mongo_session.iterate_item(database_name = 'new_database', collection_name = 'new_collection'):
        print(item)

    # drop the database.
    mongo_session['new_database'].drop()



if __name__ == '__main__':
    testcases()
