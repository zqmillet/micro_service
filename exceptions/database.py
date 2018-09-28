from exceptions import BaseException

class ConnectionTimeOut(BaseException):
    database_type = None
    host = None
    port = None
    message = 'the connection to the {database_type} {host}:{port} is timeout.'

    def __init__(self, database_type, host, port):
        self.database_type = database_type
        self.host = host
        self.port = port

class ConnectionRefusedError(BaseException):
    database_type = None
    host = None
    port = None
    message = 'the connection to the {database_type} {host}:{port} is refused.'

    def __init__(self, database_type, host, port):
        self.database_type = database_type
        self.host = host
        self.port = port

class AuthenticationError(BaseException):
    database_type = None
    host = None
    port = None
    message = 'the authentication of the {database_type} {host}:{port} is failed.'

    def __init__(self, database_type, host, port):
        self.database_type = database_type
        self.host = host
        self.port = port


