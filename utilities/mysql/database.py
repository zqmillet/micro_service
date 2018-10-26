from utilities.mysql import MySQLCollection
from utilities.function_tools import auto_type_checker

class MySQLDatabase(object):
    '''
    this class is used to manage the mysql database.

    member variables:
        - __mysql_session <utilities.mysql.MySQLSession>:
            it is the session of mysql database.

        - __database_name <str>:
            it is the database name.
    '''

    __mysql_session = None
    __database_name = None

    @auto_type_checker
    def __init__(self, database_name: str, mysql_session):
        '''
        this is the constructor of the class MySQLDatabase.

        parameters:
            - database_name:
                this is the database name.

            - mysql_session:
                this is the session of the mysql database.
        '''

        self.__mysql_session = mysql_session
        self.__database_name = database_name

    @auto_type_checker
    def fetch_collection_name_list(self) -> list:
        '''
        this function is used to get the list of collection names.

        parameters:
            nothing.

        return:
            the list of collection names.
        '''

        self.__mysql_session.execute('use {database_name};'.format(database_name = self.__database_name))
        return [item[0] for item in self.__mysql_session.execute('show tables')]

    @auto_type_checker
    def fetch_collection(self, collection_name: str) -> MySQLCollection:
        '''
        this function is used the collection whose name is collection_name.

        parameters:
            - collection_name:
                this is the name of the collection.

        return:
            the collection whose name is collection_name.
        '''

        mysql_collection = MySQLCollection(collection_name = collection_name, database_name = self.__database_name, cursor = self.__mysql_session.cursor())
        return mysql_collection

    @auto_type_checker
    def __getitem__(self, collection_name: str) -> MySQLCeollection:
        '''
        this function is used to override the __getitem__ of the class MySQLDatabase.

        parameters:
            - collection_name:
                this is the name of the collection.

        return:
            the collection whose name is collection_name.
        '''

        return self.fetch_collection(collection_name)
