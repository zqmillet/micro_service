import inspect
import functools

from utilities.webserver import Application

class Server(object):
    '''
    this class is used to manage the application.

    member variables:
        - __application <utilities.webserver.Application>:
            the application.

        - __port:
            the port the application listens.
    '''

    __application = None
    __port = None

    def __init__(self, configuration, logger, port):
        '''
        this is the constructor of the class Server.

        parameters:
            - configuration <utilities.configuration.Configuration>:
                the configuration of the server.

                for example:
                    {
                        "get_nearest_word_list": {
                            "enable":   true,
                            "api_path": "/get_nearest_word_list",
                            "function": "### from services import get_nearest_word_list; get_nearest_word_list",
                            "methods":  "get"
                        },
                        "get_word_vector": {
                            "enable":   true,
                            "api_path": "/get_word_vector",
                            "function": "### from services import get_word_vector; get_word_vector",
                            "methods":  "get/post"
                        }
                    }

            - logger <utilities.logger.Logger>:
                specify the logger for the server.

            - port <int>:
                specify the port for the server.
        '''

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
            logger.info('the service {service_name} is registed'.format(service_name = service_name))
        logger.info('all services are ready')

    def start(self):
        '''
        this function is used to start the server.

        parameters:
            nothing.

        return:
            nothing.
        '''

        self.__application.start(port = self.__port)

def convert_input_argument_type(function):
    '''
    because, the input arguments from the requests package are all string,
    this function is used to auto convert the input arguments of the function according to the function.__annotations__.

    for example:
        @convert_input_argument_type
        def add(x: int, y: int) -> str:
            return x + y

        the result of the code add(x = 3, y = '2') is '5'.
    '''

    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        for argument in kwargs:
            kwargs[argument] = function.__annotations__.get(argument, lambda x: x)(kwargs[argument])
        return function.__annotations__.get('return', lambda x: x)(function(*args, **kwargs))
    return wrapper

def testcases():
    @convert_input_argument_type
    def add(x: int, y: int) -> str:
        return x + y

    print(type(add(x = 3, y = '2')))
    print(add(x = 3, y ='2'))

if __name__ == '__main__':
    testcases()
