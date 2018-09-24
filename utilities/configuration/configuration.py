import json

from constants import FILE_MODE, ENCODE

class Configuration(dict):
    def __init__(self, argument):
        if isinstance(argument, str):
            with open(argument, FILE_MODE.READ, encoding = ENCODE.UTF8) as file:
                argument = json.loads(file.read())

        for key, value in argument.items():
            if isinstance(value, dict):
                setattr(self, key, Configuration(value))
            else:
                setattr(self, key, value)
            self[key] = value

    def __str__(self):
        return json.dumps(self, ensure_ascii = False, indent = 4)

def testcases():
    dictionary = {
        'name': 'qiqi',
        'company': {
            'name': 'huawei'
        },
        'department': {
            'name': '2012 lab'
        }
    }

    configuration = Configuration(dictionary)
    print(configuration)

    configuration = Configuration('./config/database.json')
    print(configuration)

if __name__ == '__main__':
    testcases()
