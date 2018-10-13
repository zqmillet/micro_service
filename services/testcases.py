from utilities.configuration import Configuration

def testcases():
    start(Configuration('./config/services.json'), port = 8000)

if __name__ == '__main__':
    testcases()
