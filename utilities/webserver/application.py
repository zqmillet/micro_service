import tornado.ioloop
import tornado.web

from constants import Method

class Applcation:
    __application_list = None

    def __init__(self):
        self.__application_list = list()

    def add_service(self, function, api_path, method_list):
        def member_function(self):
            self.write(function())

        import pdb; pdb.set_trace()
        class RequestHandler(tornado.web.RequestHandler):
            for method in method_list:
                setattr(self, method, member_function)

        self.__application_list.append((api_path, RequestHandler))

    def start(self, port):
        application = tornado.web.Application(self.__application_list)
        application.listen(port)
        tornado.ioloop.IOLoop.current().start()

def testcases():
    application = Applcation()
    application.add_service(function, '/hello/', method_list = [Method.get])
    application.start(port = 8000)

def function():
    return 'hello world'

if __name__ == '__main__':
    testcases()
