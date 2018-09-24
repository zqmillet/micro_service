import pymysql
import json

from utilities.mysql import MySQLDatabase

class MySQLSession:
    __session = None

    def __init__(self, host, port, username, password, charset = 'utf8'):
        self.__session = pymysql.connect(
            host       = host,
            user       = username,
            password   = password,
            port       = port,
            charset    = charset,
            autocommit = True
        )

    def execute(self, command):
        with self.__session.cursor() as cursor:
            cursor.execute(command)
            return cursor.fetchall()

    def cursor(self):
        return self.__session.cursor()

    def fetch_database_name_list(self):
        return [item[0] for item in self.execute('show databases')]

    def fetch_database(self, database_name):
        return MySQLDatabase(database_name = database_name, mysql_session = self)

    def __getitem__(self, database_name):
        return self.fetch_database(database_name)

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
