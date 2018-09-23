import tornado.web
import tornado.ioloop
import inspect

from constants import METHOD, STATUS



def create_tornado_request_handler(function, method_list):

    def get(self):
        input_arguments= {key: value[0] for key, value in self.request.arguments.items()}
        if not set(input_arguments.keys()).issubset(set(function_arguments)):
            self.write(STATUS.FAILURE)
            return
        result = function(**input_arguments)
        self.write(result)

    function_arguments = inspect.getargspec(function).args
    class RequestHandler(tornado.web.RequestHandler):
        pass
    for method in method_list:
        if method == METHOD.GET:
            setattr(RequestHandler, method, get)
    return RequestHandler


class Application:
    __service_list = None
    __application = None

    def __init__(self):
        self.__service_list = list()

    def regist_service(self, function, api_path, method_list):
        RequestHandler = create_tornado_request_handler(function, method_list = [METHOD.GET])
        self.__service_list.append(
            (api_path, RequestHandler)
        )

    def start(self, port):
        self.__application = tornado.web.Application(self.__service_list)
        self.__application.listen(port)
        tornado.ioloop.IOLoop.instance().start()

def testcases():
    def add(x, y = '1'):
        x = int(x)
        y = int(y)
        return str(x + y)

    application = Application()
    application.regist_service(add, api_path = '/add', method_list = [METHOD.GET])
    application.start(port = 8000)

if __name__ == '__main__':
    testcases()

