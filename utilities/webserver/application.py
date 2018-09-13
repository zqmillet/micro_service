import tornado.ioloop
import tornado.web

class Applcation:
    __application_list = None

    def __init__(self):
        self.__application_list = list()

    def add_service(self, function, api_path, method_list):
        pass

    def start(self, port):
        pass

def testcases():
    application = Applcation()

if __name__ == '__main__':
    testcases()
