from resources.now import now

def get_server_time():
    return str(now)

def testcases():
    print(get_server_time())

if __name__ == '__main__':
    testcases()
