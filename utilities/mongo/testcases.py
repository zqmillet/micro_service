from utilities.mongo import MongoSession
from exceptions import ConnectionRefusedError, ConnectionTimeOut

def testcases():
    try:
        mongo_session = MongoSession(
            host     = '8.8.8.8', # wrong host.
            port     = 27017,
            username = 'admin',
            password = 'admin'
        )
    except Exception as e:
        print(e)

    try:
        mongo_session = MongoSession(
            host     = 'localhost',
            port     = 2701, # wrong port.
            username = 'admin',
            password = 'admin'
        )
    except Exception as e:
        print(e)

    try:
        mongo_session = MongoSession(
            host     = 'localhost',
            port     = 27017,
            username = 'username', # wrong username.
            password = 'password' # wrong password.
        )
    except Exception as e:
        print(e)


    # from utilities.configuration import Configuration
    # configuration = Configuration('./config/database.json')

    # # create a mongo database session.
    # try:
    #     mongo_session = MongoSession(**configuration.mongo)
    # except ConnectionRefusedError as e:
    #     print(e)


    # # create a new database, and create a new collection, then insert 10 items
    # # into the new collection.
    # for index in range(10):
    #     mongo_session['new_database']['new_collection'].insert(
    #         {
    #             'index': index,
    #             'name': 'test item {index}'.format(index = index)
    #         }
    #     )

    # # print the new items.
    # for item in mongo_session['new_database']['new_collection']:
    #     print(item)

    # # change the name of the new items, and add new property for each item.
    # for index, item in enumerate(mongo_session['new_database']['new_collection']):
    #     item['name'] = 'item {index}'.format(index = index)
    #     item['height'] = index

    # # print the new items.
    # for item in mongo_session['new_database']['new_collection']:
    #     print(item)

    # # drop the database.
    # mongo_session['new_database'].drop()

if __name__ == '__main__':
    testcases()
