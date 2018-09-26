import json
import os

from constants import FILE_MODE, ENCODE
from exceptions import FileDoesNotExistError, TypeError
from utilities.configuration import execute

class Configuration(dict):
    '''
    this class is used to manage the configuration from json file.
    '''

    # if a value starts with __code_prefix, it is a python code.
    __code_prefix = None

    def __init__(self, argument, code_prefix = '###'):
        '''
        this is the constructor of the class Configuration.

        parameters:
            - argument:
                this is the input argument.
                if its type is str, it will be regarded as a json file path;
                if its type is dict, it will be regarded as a dictionary.

            - code_prefix:
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
                setattr(self, key, Configuration(value, code_prefix = self.__code_prefix))
            else:
                if isinstance(value, str) and value.startswith(self.__code_prefix):
                    value = execute(value.strip(self.__code_prefix).strip())
                setattr(self, key, value)
            self[key] = value
