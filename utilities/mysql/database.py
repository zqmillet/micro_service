from utilities.mysql import MySQLCollection

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
