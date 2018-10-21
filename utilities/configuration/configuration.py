import json
import os

from constants import FILE_MODE, ENCODE
from exceptions import FileDoesNotExistError
from utilities.configuration import execute
from utilities.function_tools import auto_type_checker

class Configuration(dict):
    '''
    this class is used to manage the configuration from json file.
    '''

    # if a value starts with __code_prefix, it is a python code.
    __code_prefix = None

    @auto_type_checker
    def __init__(self, argument: (str, dict), code_prefix: str = '###', auto_execute: bool = False):
        '''
        this is the constructor of the class Configuration.

        parameters:
            - argument:
                this is the input argument.
                if its type is str, it will be regarded as a json file path;
                if its type is dict, it will be regarded as a dictionary.

            - code_prefix:
                if a value starts with code_prefix, it is a python code.

            - auto_execute:
                if auto_execute is True, this class will auto execute the value which startswith the code_prefix.

        exceptions:
            - FileDoesNotExistError:
                if the input file does not exist, this error will be thrown.
        '''

        self.__code_prefix = code_prefix

        if isinstance(argument, str):
            if not os.path.isfile(argument):
                raise FileDoesNotExistError(file_path = argument)

            with open(argument, FILE_MODE.READ, encoding = ENCODE.UTF8) as file:
                argument = json.loads(file.read())

        for key, value in argument.items():
            if isinstance(value, dict):
                value = Configuration(value, code_prefix = self.__code_prefix, auto_execute = auto_execute)
            elif auto_execute:
                value = execute(value.strip(self.__code_prefix).strip())
            setattr(self, key, value)
            self[key] = value

    def execute(self):
        '''
        this function is used the execute the value which startswith the code_prefix.
        '''

        for key in self:
            value = self[key]
            if isinstance(value, str) and value.startswith(self.__code_prefix):
                value = execute(value.strip(self.__code_prefix).strip())
            elif isinstance(value, Configuration):
                value.execute()
            else:
                pass

            self[key] = value
            setattr(self, key, value)

