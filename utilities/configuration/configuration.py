import json
import os

from constants import FILE_MODE, ENCODE
from exceptions import FileDoesNotExistError, TypeError
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
            - argument <str>/<dict>:
                this is the input argument.
                if its type is str, it will be regarded as a json file path;
                if its type is dict, it will be regarded as a dictionary.

            - code_prefix <str>:
                if a value starts with code_prefix, it is a python code.

        exceptions:
            - FileDoesNotExistError:
                if the input file does not exist, this error will be thrown.

            - TypeError:
                if the argument is not a dictionary, this error will be thrown.
        '''

        self.__code_prefix = code_prefix

        if isinstance(argument, str):
            if not os.path.isfile(argument):
                raise FileDoesNotExistError(file_path = argument)

            with open(argument, FILE_MODE.READ, encoding = ENCODE.UTF8) as file:
                argument = json.loads(file.read())

        if not isinstance(argument, dict):
            raise TypeError(type(argument))

        for key, value in argument.items():
            if isinstance(value, dict):
                value = Configuration(value, code_prefix = self.__code_prefix, auto_execute = auto_execute)
            elif auto_execute:
                value = execute(value.strip(self.__code_prefix).strip())
            setattr(self, key, value)
            self[key] = value

    def execute(self):
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

