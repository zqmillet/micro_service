import inspect
import functools

from utilities.webserver import Application

class Server(object):
    __application = None
    __port = None

    def __init__(self, configuration, logger, port):
        self.__application = Application(logger = logger)
        self.__port = port

        for service_name in configuration.keys():
            service_information = getattr(configuration, service_name)
            if not service_information.enable:
                continue
            self.__application.regist_service(
                function    = convert_input_argument_type(getattr(configuration, service_name).function),
                api_path    = service_information.api_path,
                method_list = service_information.methods.split('/')
            )

    def start(self):
        self.__application.start(port = self.__port)

def convert_input_argument_type(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        for argument in kwargs:
            kwargs[argument] = function.__annotations__[argument](kwargs[argument])
        return function.__annotations__.get('return', lambda x: x)(function(*args, **kwargs))
    return wrapper
