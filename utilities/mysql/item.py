import json

from utilities.mysql import MySQLValue, value_to_string
from utilities.function_tools import auto_type_checker

class MySQLItem:
    '''
    '''

    __item_dictionary = None
    __type_dictionary = None
    __cursor = None

    __database_name = None
    __collection_name = None
    __collection = None

    @auto_type_checker
    def __init__(self, column_list: list, type_list: list, value_list: (list, tuple), database_name: str, collection_name: str, collection, cursor):
        self.__cursor = cursor
        self.__database_name = database_name
        self.__collection_name = collection_name
        self.__type_list = type_list
        self.__collection = collection

        self.__item_dictionary = dict()

        for column, type, value in zip(column_list, type_list, value_list):
            self.__item_dictionary[column] = MySQLValue(value = value, type = type)

    @auto_type_checker
    def __str__(self) -> str:
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
