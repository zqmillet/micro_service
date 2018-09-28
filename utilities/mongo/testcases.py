from utilities.mongo import MongoSession

def testcases():
    from utilities.configuration import Configuration
    configuration = Configuration('./config/database.json')

    # create a mongo database session.
    mongo_session = MongoSession(**configuration.mongo)

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
    for item in mongo_session['new_database']['new_collection']:
        print(item)

    # change the name of the new items, and add new property for each item.
    for index, item in enumerate(mongo_session['new_database']['new_collection']):
        item['name'] = 'item {index}'.format(index = index)
        item['height'] = index

    # print the new items.
    for item in mongo_session['new_database']['new_collection']:
        print(item)

    # drop the database.
    mongo_session['new_database'].drop()

if __name__ == '__main__':
    testcases()
