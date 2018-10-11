import tornado.web
import tornado.ioloop
import inspect
import json

from constants import METHOD, STATUS, ENCODE

def create_tornado_request_handler(function, method_list, logger):
    def get(self):
        input_arguments= {key: value[0] for key, value in self.request.arguments.items()}
        if not set(input_arguments.keys()).issubset(set(function_arguments)):
            self.write(STATUS.FAILURE)
            return
        result = function(**input_arguments)
        self.write(result)

        if not logger is None:
            logger.info('the function {function_name} is called by get.'.format(function_name = function.__name__))

    def post(self):
        body = self.request.body.decode(ENCODE.UTF8)

        if body == '':
            input_arguments = dict()
        else:
            input_arguments = json.loads(body)

        result = function(**input_arguments)
        self.write(result)

        if not logger is None:
            logger.info('the function {function_name} is called by post.'.format(function_name = function.__name__))

    function_arguments = inspect.getargspec(function).args

    class RequestHandler(tornado.web.RequestHandler):
        pass

    for method in method_list:
        if method == METHOD.GET:
            setattr(RequestHandler, method, get)
        if method == METHOD.POST:
            setattr(RequestHandler, method, post)

    return RequestHandler

class Application:
    __service_list = None
    __application  = None
    __logger       = None

    def __init__(self, logger = None):
        self.__service_list = list()
        self.__logger = logger

    def regist_service(self, function, api_path, method_list):
        RequestHandler = create_tornado_request_handler(function, method_list = method_list, logger = self.__logger)
        self.__service_list.append(
            (api_path, RequestHandler)
        )

    def start(self, port):
        self.__application = tornado.web.Application(self.__service_list)
        self.__application.listen(port)
        tornado.ioloop.IOLoop.instance().start()
