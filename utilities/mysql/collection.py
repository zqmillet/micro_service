from utilities.mysql import MySQLItem, value_to_string

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
