import pymysql
import json

class MySQLSession:
    __session = None

    def __init__(self, host, port, username, password, charset = 'utf8'):
        self.__session = pymysql.connect(
            host     = host,
            user     = username,
            password = password,
            port     = port,
            charset  = charset
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

    def commit(self):
        self.__session.commit()

class MySQLDatabase:
    __mysql_session = None
    __database_name = None

    def __init__(self, database_name, mysql_session):
        self.__mysql_session = mysql_session
        self.__database_name = database_name

    def fetch_collection_name_list(self):
        self.__mysql_session.execute('use {database_name}'.format(database_name = self.__database_name))
        return [item[0] for item in self.__mysql_session.execute('show tables')]

    def fetch_collection(self, collection_name):
        mysql_collection = MySQLCollection(collection_name = collection_name, database_name = self.__database_name, cursor = self.__mysql_session.cursor())
        return mysql_collection

    def execute(self, command):
        self.__mysql_session.execute(command)

class MySQLCollection:
    __cursor = None
    __database_name = None
    __collection_name = None
    __item_list = None

    def __init__(self, collection_name, database_name, cursor):
        self.__collection_name = collection_name
        self.__database_name = database_name
        self.__cursor = cursor
        self.__item_list = list()

        self.__cursor.execute('use {database_name}'.format(database_name = database_name))
        self.__cursor.execute('describe {collection_name}'.format(collection_name = collection_name))
        column_list = [item[0] for item in self.__cursor.fetchall()]

        self.__cursor.execute('select * from {collection_name}'.format(collection_name = collection_name))
        value_list_list = self.__cursor.fetchall()

        for index, value_list in enumerate(value_list_list):
            self.__item_list.append(
                MySQLItem(
                    column_list     = column_list,
                    value_list      = value_list,
                    index           = index,
                    database_name   = self.__database_name,
                    collection_name = self.__collection_name,
                    cursor          = self.__cursor
                )
            )

    def __iter__(self):
        for item in self.__item_list:
            yield item

class MySQLItem:
    __dictionary = None
    __cursor = None
    __database_name = None
    __collection_name = None
    __index = None

    def __init__(self, column_list, value_list, index, database_name, collection_name, cursor):
        self.__cursor = cursor
        self.__database_name = database_name
        self.__collection_name = collection_name
        self.__index = index
        self.__dictionary = dict()

        for column, value in zip(column_list, value_list):
            self.__dictionary[column] = value

    def __str__(self):
        return json.dumps(self.__dictionary, ensure_ascii = False)

    def set(self, key, value):
        self.__cursor.execute('use {database_name}'.format(database_name = self.__database_name))
        self.__cursor.rownumber = self.__index + 1
        sql_command = 'update {collection_name} set {key} = {value} limit 1;'.format(collection_name = self.__collection_name, key = key, value = value)
        self.__cursor.execute(sql_command)

def testcases():
    mysql_session = MySQLSession(
        host = '127.0.0.1',
        username = 'root',
        password = 'root',
        port = 3306
    )

    # print(mysql_session['mysql'].fetch_collection_name_list())
    collection = mysql_session['Test'].fetch_collection('tabu')
    for index, item in enumerate(collection):
        print(item)
        item.set('test1', index + 3)

    mysql_session.commit()

if __name__ == '__main__':
    testcases()
