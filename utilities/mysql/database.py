from utilities.mysql import MySQLCollection
from utilities.function_tools import auto_type_checker

class MySQLDatabase:
    __mysql_session = None
    __database_name = None

    @auto_type_checker
    def __init__(self, database_name: str, mysql_session):
        self.__mysql_session = mysql_session
        self.__database_name = database_name

    @auto_type_checker
    def fetch_collection_name_list(self) -> str:
        self.__mysql_session.execute('use {database_name};'.format(database_name = self.__database_name))
        return [item[0] for item in self.__mysql_session.execute('show tables')]

    @auto_type_checker
    def fetch_collection(self, collection_name: str) -> MySQLCollection:
        mysql_collection = MySQLCollection(collection_name = collection_name, database_name = self.__database_name, cursor = self.__mysql_session.cursor())
        return mysql_collection

    @auto_type_checker
    def __getitem__(self, collection_name: str) -> MySQLCollection:
        return self.fetch_collection(collection_name)
