import tornado.web
import tornado.ioloop
import inspect
import json
import logging

from constants import METHOD, STATUS, ENCODE

def create_tornado_request_handler(function, method_list, logger):
    def get(self):
        input_arguments= {key: value[0].decode(ENCODE.UTF8) for key, value in self.request.arguments.items()}
        try:
            result = function(**input_arguments)
            self.write(result)
            logger.info('the function {function_name} is called by get.'.format(function_name = function.__name__))
        except Exception as e:
            self.set_status(400)
            logger.error(e.args[0])

    def post(self):
        body = self.request.body.decode(ENCODE.UTF8)

        if body == '':
            input_arguments = dict()
        else:
            input_arguments = json.loads(body)

        try:
            result = function(**input_arguments)
            self.write(result)
            logger.info('the function {function_name} is called by post.'.format(function_name = function.__name__))
        except Exception as e:
            self.set_status(400)
            logger.error(e.args[0])

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

    def __init__(self, logger):
        tornado_access_logger = logging.getLogger('tornado.access')
        tornado_access_logger.addHandler(logging.NullHandler())
        tornado_access_logger.propagate = False

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
