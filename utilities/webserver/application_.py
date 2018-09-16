import tornado.web
import tornado.ioloop
import json
import time
import inspect
from constants import Encode, Method, Status
from utilities.logger import logger

# this function is a class decorator, its input is a function, and its output is a class with function as its member method.
def create_tornado_request_handler(function, method_list):
    # definition of the get method for request handler.
    def get(self):
        now = time.time()

        # first, get the input parameters and values of the function.
        argument_dictionary = dict()
        for argument in self.request.arguments:
            argument_dictionary[argument] = self.request.arguments[argument][0]

        request_argument_set = set(self.request.arguments.keys())
        function_argument_set = set(inspect.getargspec(function).args)
        if not request_argument_set.issubset(function_argument_set):
            self.finish(Status.failure)
            illegal_parameter_list = list(request_argument_set - function_argument_set)
            logger.error('there is/are illegal parameter(s): {illegal_parameters}.'.format(illegal_parameters = ', '.join(illegal_parameter_list)))
            return

        import pdb; pdb.set_trace()
        # then, call the function by passing the input parameters.
        result = function(**argument_dictionary)
        self.finish(result)
        logger.info('function \'{name}\' is called by get, the time consumed is {consumed_time} second(s)'.format(name = function.__name__, consumed_time = time.time() - now))

    # definition of the options method for request handler.
    def options(self):
        # return nothing.
        self.finish(None)

    # definition of the post method for request handler.
    def post(self):
        now = time.time()

        # first, the the parameters from request body.
        body = self.request.body.decode(Encode.utf8)
        if body == '':
            post_data = dict()
        else:
            post_data = json.loads(body)

        # get the result, and return it.
        result = function(**post_data)
        self.finish(result)
        logger.info('function \'{name}\' is called by post, the time consumed is {consumed_time} second(s)'.format(name = function.__name__, consumed_time = time.time() - now))

    # get the argument list of function.
    function_arguments = inspect.getargspec(function).args

    # initialize a class witch inherits from tornado.web.RequestHandler.
    class Class(tornado.web.RequestHandler):
        # this function is used to add headers into request.
        def set_default_headers(self):
            origin = self.request.headers.get('Origin')
            if origin:
                self.set_header('Access-Control-Allow-Origin', origin)
            self.set_header('Access-Control-Allow-Credentials', 'true')
            self.set_header('Access-Control-Allow-Headers', 'Content-Type,Access-Token,UserName,RequestId,ClientType')

    # add function_arguments into member variables of this class.
    setattr(Class, 'function_arguments', function_arguments)
    # add methods in method_list into member functions of this class.
    for method in method_list:
        if method == Method.get:
            setattr(Class, Method.get, get)
        if method == Method.options:
            setattr(Class, Method.options, options)
        if method == Method.post:
            setattr(Class, Method.post, post)

    # finish this class, and return it.
    return Class

# this class is used to manage many services by using tornado.
class Application:
    # service list.
    __service_list = None
    # application.
    __application = None

    # constructor.
    def __init__(self):
        self.__service_list = list()

    # def __new__(cls, *args, **kwargs):
    #     if not hasattr(cls, '_instance'):
    #         cls._instance = super().__new__(cls)
    #     return cls._instance

    # this function is used to regist service by api path and method list.
    def regist_service(self, api_path, method_list):
        def _add_service(function):
            Class = create_tornado_request_handler(function, method_list)
            self.__service_list.append((api_path, Class))
            logger.info('the {function_name} is registed, the api path is {api_path}, method(s) is/are {methods}'.format(function_name = function.__name__, api_path = api_path, methods = ', '.join(method_list)))
        return _add_service

    def add_service(self, function, api_path, method_list):
        Class = create_tornado_request_handler(function, method_list)
        self.__service_list.append((api_path, Class))
        logger.info('the {function_name} is added, the api path is {api_path}, method(s) is/are {methods}'.format(function_name = function.__name__, api_path = api_path, methods = ', '.join(method_list)))

    # this function is used to start this application on specific port.
    def start(self, port):
        port = int(port)
        self.__application = tornado.web.Application(self.__service_list)
        self.__application.listen(port)
        logger.info('the application is started')
        tornado.ioloop.IOLoop.instance().start()
