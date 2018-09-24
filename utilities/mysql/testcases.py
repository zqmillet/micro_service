from utilities.mysql import MySQLSession

def testcases():
    from utilities.configuration import Configuration
    configuration = Configuration('./config/database.json')

    mysql_session = MySQLSession(**configuration.mysql)

    collection = mysql_session['new_database']['new_collection']
    for number in range(10):
        collection.append(
            {
                'number': number,
                'name': 'test item {number}'.format(number = number)
            }
        )

    for item in collection:
        print(item)

    for item in collection:
        item['name'] = 'item {number}'.format(number = item['number'])
        item['number'] = item['number'] + 1

    for item in collection:
        print(item)

    for item in collection:
        item.drop()

if __name__ == '__main__':
    testcases()
