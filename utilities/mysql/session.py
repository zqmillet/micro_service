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
            charset  = charset,
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

    def commit(self):
        pass

class MySQLDatabase:
    __mysql_session = None
    __database_name = None

    def __init__(self, database_name, mysql_session):
        self.__mysql_session = mysql_session
        self.__database_name = database_name

    def fetch_collection_name_list(self):
        self.__mysql_session.execute('use {database_name};'.format(database_name = self.__database_name))
        return [item[0] for item in self.__mysql_session.execute('show tables')]

    def fetch_collection(self, collection_name):
        mysql_collection = MySQLCollection(collection_name = collection_name, database_name = self.__database_name, cursor = self.__mysql_session.cursor())
        return mysql_collection

    def __getitem__(self, collection_name):
        return self.fetch_collection(collection_name)

    def execute(self, command):
        self.__mysql_session.execute(command)

class MySQLCollection:
    __cursor = None
    __database_name = None
    __collection_name = None
    __item_list = None

    __column_list = None
    __type_list = None

    def __init__(self, collection_name, database_name, cursor):
        self.__collection_name = collection_name
        self.__database_name = database_name
        self.__cursor = cursor
        self.__item_list = list()

        command = 'use {database_name};'.format(
            database_name = database_name
        )
        self.__cursor.execute(command)

        command = 'describe {collection_name};'.format(
            collection_name = collection_name
        )
        self.__cursor.execute(command)

        column_description_list = self.__cursor.fetchall()
        self.__column_list = [item[0] for item in column_description_list]
        self.__type_list   = [item[1] for item in column_description_list]

        command = 'select * from {collection_name};'.format(
            collection_name = collection_name
        )
        self.__cursor.execute(command)

        value_list_list = self.__cursor.fetchall()

        for value_list in value_list_list:
            self.__item_list.append(
                MySQLItem(
                    value_list      = value_list,
                    column_list     = self.__column_list,
                    type_list       = self.__type_list,
                    database_name   = self.__database_name,
                    collection_name = self.__collection_name,
                    cursor          = self.__cursor,
                    collection      = self
                )
            )

    def drop(self):
        command = 'use {database_name};'.format(
            database_name = self.__database_name
        )
        self.__cursor.execute(command)

        command = 'drop table {collection_name};'.format(
            collection_name = self.__collection_name
        )
        self.__cursor.execute(command)

    def __iter__(self):
        for item in list(self.__item_list):
            yield item

    def delete_item(self, item):
        self.__item_list.remove(item)

    def append(self, item_dictionary):
        if not set(self.__column_list) == set(item_dictionary.keys()):
            return

        column_list = list()
        value_list = list()
        for key, value in item_dictionary.items():
            column_list.append(key)
            value_list.append(value_to_string(value))

        column_tuple_string = '(' + ', '.join(column_list) + ')'
        value_tuple_string = '(' + ', '.join(value_list) + ')'
        command = 'insert into {collection_name} {column_tuple_string} values {value_tuple_string};'.format(
            collection_name = self.__collection_name,
            column_tuple_string = column_tuple_string,
            value_tuple_string = value_tuple_string
        )
        self.__cursor.execute(command)

        self.__item_list.append(
            MySQLItem(
                value_list      = [item_dictionary[column] for column in self.__column_list],
                column_list     = self.__column_list,
                type_list       = self.__type_list,
                database_name   = self.__database_name,
                collection_name = self.__collection_name,
                cursor          = self.__cursor,
                collection      = self
            )
        )

class MySQLItem:
    __item_dictionary = None
    __type_dictionary = None
    __cursor = None

    __database_name = None
    __collection_name = None
    __collection = None

    def __init__(self, column_list, type_list, value_list, database_name, collection_name, collection, cursor):
        self.__cursor = cursor
        self.__database_name = database_name
        self.__collection_name = collection_name
        self.__type_list = type_list
        self.__collection = collection

        self.__item_dictionary = dict()

        for column, type, value in zip(column_list, type_list, value_list):
            self.__item_dictionary[column] = MySQLValue(value = value, type = type)

    def __str__(self):
        return json.dumps({key: value.evaluate() for key, value in self.__item_dictionary.items()}, ensure_ascii = False)

    def drop(self):
        command = 'use {database_name};'.format(
            database_name = self.__database_name
        )
        self.__cursor.execute(command)

        command = 'delete from {collection_name} where {condition} limit 1;'.format(
            collection_name = self.__collection_name,
            condition = self.__condition()
        )
        self.__cursor.execute(command)
        self.__collection.delete_item(self)

    def __getitem__(self, key):
        return self.__item_dictionary[key].evaluate()

    def __setitem__(self, key, value):
        command = 'use {database_name};'.format(
            database_name = self.__database_name
        )
        self.__cursor.execute(command)

        command = 'update {collection_name} set {key} = {value} where {condition} limit 1;'.format(
            collection_name = self.__collection_name,
            key             = key,
            value           = value_to_string(value),
            condition       = self.__condition()
        )
        self.__cursor.execute(command)

        old_value = self.__item_dictionary[key]
        self.__item_dictionary[key] = MySQLValue(value = value, type = old_value.get_type())

    def __condition(self):
        condition_list = list()
        for key, value in self.__item_dictionary.items():
            condition_list.append(
                '{key} = {value}'.format(
                    key = key,
                    value = str(value)
                )
            )
        return ' and '.join(condition_list)


class MySQLValue:
    __type = None
    __value = None

    def __init__(self, value, type):
        self.__type = type
        self.__value = value

    def evaluate(self):
        type = fetch_python_type(self.__type)
        return type(self.__value)

    def __str__(self):
        python_type = fetch_python_type(self.__type)
        return value_to_string(python_type(self.__value))

    def get_type(self):
        return self.__type

def value_to_string(value):
    if isinstance(value, str):
        prefix = '"'
        suffix = '"'
    else:
        prefix = ''
        suffix = ''
    return '{prefix}{value}{suffix}'.format(
        prefix = prefix,
        value = value,
        suffix = suffix
    )

def fetch_python_type(mysql_type):
    mysql_type = mysql_type.split('(')[0]
    type_dictionary = {
        int:   ['tinyint', 'smallint', 'mediumint', 'int', 'bigint', 'bit'],
        float: ['float', 'double', 'decimal'],
        str:   ['char', 'varchar', 'tinytext', 'text', 'mediumtext', 'longtext']
    }

    for python_type, mysql_type_string_list in type_dictionary.items():
        if mysql_type in mysql_type_string_list:
            return python_type
    return lambda x: x

def testcases():
    mysql_session = MySQLSession(
        host     = 'localhost',
        username = 'root',
        password = 'root',
        port     = 3306
    )

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
