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

    print('initialize the configuration with a dictionary.')
    configuration = Configuration(dictionary)

    print('the configuration is:')
    print(configuration)

    print('the configuration.company.name is:')
    print(configuration.company.name)

    print('the configuration.department is:')
    print(configuration.department)

    print('-' * 40)
    print('initialize the configuration with a file.')
    configuration = Configuration('./config/database.json')

    print('the configuration is:')
    print(configuration)

    print('-' * 40)
    print('initialize the configuration with a file who has python code.')
    configuration = Configuration('./config/math.json')

    print('the configuration is:')
    print(configuration)

    print(configuration.exp(1))
    print(configuration.square(2))

if __name__ == '__main__':
    testcases()
