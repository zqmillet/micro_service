from utilities.configuration import Configuration

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
    print(configuration.name)
    print(configuration.company.name)
    print(configuration.department)

    configuration = Configuration('./config/database.json')
    print(configuration)

    configuration = Configuration('./config/math.json')
    print(configuration)

if __name__ == '__main__':
    testcases()
