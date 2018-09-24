import json

class Configuration(dict):
    def __init__(self, dictionary):
        for key, value in dictionary.items():
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

if __name__ == '__main__':
    testcases()
