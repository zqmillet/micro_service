class Configuration:
    def __init__(self, dictionary):
        pass

def dictionary_to_instance(dictionary):
    class Object:
        pass
    for key, value in dictionary.items():
        if isinstance(value, dict):
            setattr(Object, key, dictionary_to_instance(value))
        else:
            setattr(Object, key, value)
    return Object()

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

    instance = dictionary_to_instance(dictionary)
    import pdb; pdb.set_trace()

if __name__ == '__main__':
    testcases()
