from exceptions import BaseException

class DatabaseConnectionError(BaseException):
    username = None
    password = None
    host     = None
    port     = None

    massage = 'there is an error while connecting to the database "{username}:{password}@{host}:{port}."

    def __init__(self, host, port, username, password):
        self.host     = host
        self.port     = port
        self.username = username
        self.password = password

