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
    import pdb; pdb.set_trace()

if __name__ == '__main__':
    testcases()
