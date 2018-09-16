import tornado.web
import tornado.ioloop
import inspect

from constants import Encode, Method, Status

def create_tornado_request_handler(function, method_list):
    function_arguments = inspect.getargspec(function).args

    import pdb; pdb.set_trace()
    class RequestHandler(tornado.web.RequestHandler):
        pass

    return RequestHandler


class Application:
    service_list = None

    def __init__(self):
        self.service_list = list()

    def regist_service(self, function, api_path, method_list):
        pass

def testcases():
    def add(x, y):
        return x + y
    RequestHandler = create_tornado_request_handler(add, method_list = [Method.get])

if __name__ == '__main__':
    testcases()

