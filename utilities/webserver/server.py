import json
import inspect
import functools

from utilities.configuration import Configuration
from utilities.webserver import Application
from utilities.scheduler import Scheduler
from utilities.function_tools import auto_type_checker
from constants import FILE_MODE, ENCODE

class Server(object):
    '''
    this class is used to manage the application.

    member variables:
        - __application <utilities.webserver.Application>:
            the application.

        - __scheduler <utilities.scheduler.Scheduler>:
            the scheduler.

        - __port <int>:
            the port the application listens.
    '''

    __application = None
    __scheduler = None
    __port = None

    def __init__(self, configuration_file_path, logger, port):
        '''
        this is the constructor of the class Server.

        parameters:
            - configuration_file_path:
                the configuration file path of the server.

            - logger:
                specify the logger for the server.

            - port:
                specify the port for the server.
        '''

        self.__application = Application(logger = logger)
        self.__scheduler = Scheduler(logger = logger)
        self.__port = port

        with open(configuration_file_path, FILE_MODE.READ, encoding = ENCODE.UTF8) as file:
            service_information_list = json.loads(file.read())

        for service_information in service_information_list:
            configuration = Configuration(service_information)

            if not configuration.enable:
                continue
            configuration.execute()

            if 'api_path' in configuration and 'methods' in configuration:
                self.__application.regist_service(
                    function    = convert_input_argument_type(configuration.function),
                    api_path    = configuration.api_path,
                    method_list = configuration.methods
                )

            if 'triggers' in configuration:
                for trigger in configuration.triggers:
                    self.__scheduler.add_task(configuration.function, **trigger)

            logger.info('the service {service_name} is registed'.format(service_name = configuration.name))
        logger.info('all services are ready')

    def start(self):
        '''
        this function is used to start the server.

        parameters:
            nothing.

        return:
            nothing.
        '''

        self.__scheduler.start()
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
