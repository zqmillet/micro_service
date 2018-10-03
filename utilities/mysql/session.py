import pymysql
import json

from utilities.mysql import MySQLDatabase
from constants import ENCODE

class MySQLSession:
    '''
    this class is used manage the mysql database.

    member variables:
        - __session <pymysql.connections.Connection>:
            it is used to manage the mysql connection.
    '''

    __session = None

    def __init__(self, host, port, username, password, charset = ENCODE.UTF8):
        '''
        this is the constructor of the class MySQLSession.

        parameters:
            - host <str>:
                the ip address of the mysql host.

            - post <int>:
                the port of the mysql host.

            - username <str>:
                the username of the mysql database.

            - password <str>:
                the password of the mysql database.

            - charset <str>:
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

    def execute(self, command):
        '''
        this function is used to execute the command.

        parameters:
            - command <str>:
                the command will be executed.

        return <tuple>:
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

    def fetch_database_name_list(self):
        '''
        this function is used to fetch the list of database names of mysql.

        parameters:
            nothing.

        return <list>:
            the list of database names.
        '''

        return [item[0] for item in self.execute('show databases')]

    def fetch_database(self, database_name):
        '''
        this function is used to fetch the database according to the database name.

        parameters:
            - database_name <str>:
                the name of database.

        return <MySQLDatabase>:
            the database whose name is database_name.
        '''

        return MySQLDatabase(database_name = database_name, mysql_session = self)

    def __getitem__(self, database_name):
        '''
        this function is used to override the function __getitem__.

        parameters:
            - database_name <str>:
                the name of database.

        return <MySQLDatabase>:
            the database whose name is database_name.
        '''

        return self.fetch_database(database_name)
