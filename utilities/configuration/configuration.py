import json

from constants import FILE_MODE, ENCODE
from utilities.configuration import execute

class Configuration(dict):
    __prefix = ''

    def __init__(self, argument, prefix = '###'):
        self.__prefix = prefix

        if isinstance(argument, str):
            with open(argument, FILE_MODE.READ, encoding = ENCODE.UTF8) as file:
                argument = json.loads(file.read())

        for key, value in argument.items():
            if isinstance(value, dict):
                setattr(self, key, Configuration(value, prefix = self.__prefix))
            else:
                if isinstance(value, str) and value.startswith(self.__prefix):
                    setattr(self, key, execute(value.strip(self.__prefix).strip()))
                else:
                    setattr(self, key, value)
            self[key] = value

    def __str__(self):
        return json.dumps(self, ensure_ascii = False, indent = 4)
