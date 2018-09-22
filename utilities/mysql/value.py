from utilities.mysql import fetch_python_type, value_to_string

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
