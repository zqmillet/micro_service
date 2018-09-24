import json

class Configuration:
    def __init__(self, dictionary):
        for key, value in dictionary.items():
            if isinstance(value, dict):
                setattr(self, key, Configuration(value))
            else:
                setattr(self, key, value)

    def to_dictionary(self):
        keys = [item for item in self.__dir__() if not item.startswith('__') and not callable(getattr(self, item))]
        dictionary = dict()
        for key in keys:
            value = getattr(self, key)
            if isinstance(value, Configuration):
                dictionary[key] = value.to_dictionary()
            else:
                dictionary[key] = value
        return dictionary

    def __str__(self):
        return json.dumps(self.to_dictionary(), ensure_ascii = False, indent = 4)

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

if __name__ == '__main__':
    testcases()
