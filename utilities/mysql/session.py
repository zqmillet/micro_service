import pymysql
import json

from utilities.mysql import MySQLDatabase
from utilities.function_tools import auto_type_checker
from constants import ENCODE

class MySQLSession:
    '''
    this class is used manage the mysql database.

    member variables:
        - __session <pymysql.connections.Connection>:
            it is used to manage the mysql connection.
    '''

    __session = None

    @auto_type_checker
    def __init__(self, host: str, port: int, username: str, password: str, charset: str = ENCODE.UTF8):
        '''
        this is the constructor of the class MySQLSession.

        parameters:
            - host:
                the ip address of the mysql host.

            - post:
                the port of the mysql host.

            - username:
                the username of the mysql database.

            - password:
                the password of the mysql database.

            - charset:
                the charset of the mysql database.
                the default value is utf8.
        '''

        self.__session = pymysql.connect(
            host       = host,
            user       = username,
            password   = password,
            port       = port,
            charset    = charset,
            autocommit = True
        )

    @auto_type_checker
    def execute(self, command: str) -> tuple:
        '''
        this function is used to execute the command.

        parameters:
            - command:
                the command will be executed.

        return:
            the results of the command.
        '''

        with self.__session.cursor() as cursor:
            cursor.execute(command)
            import pdb; pdb.set_trace()
            return cursor.fetchall()

    def cursor(self):
        '''
        this function is used to fetch the cursor of the connection.

        parameters:
            nothing.

        return <pymysql.cursors.Cursor>:
            the cursor object.
        '''

        return self.__session.cursor()

    @auto_type_checker
    def fetch_database_name_list(self) -> list:
        '''
        this function is used to fetch the list of database names of mysql.

        parameters:
            nothing.

        return:
            the list of database names.
        '''

        return [item[0] for item in self.execute('show databases')]

    @auto_type_checker
    def fetch_database(self, database_name: str) -> MySQLDatabase:
        '''
        this function is used to fetch the database according to the database name.

        parameters:
            - database_name <str>:
                the name of database.

        return <MySQLDatabase>:
            the database whose name is database_name.
        '''

        return MySQLDatabase(database_name = database_name, mysql_session = self)

    @auto_type_checker
    def __getitem__(self, database_name: str) -> MySQLDatabase:
        '''
        this function is used to override the function __getitem__.

        parameters:
            - database_name <str>:
                the name of database.

        return <MySQLDatabase>:
            the database whose name is database_name.
        '''

        return self.fetch_database(database_name)
