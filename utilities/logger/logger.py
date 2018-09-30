import os
import logging
import logging.config
import datetime

from utilities.logger import get_handler
from constants import LOGGING_LEVEL, LOGGING_HANDLER, LOGGING_FORMAT

class Logger:
    '''
    this class is used for logging.

    member variables:
        - __logger <logging.Logger>:
            this is the logger.
    '''

    __logger = None

    def __init__(
        self,
        main_title   = 'root',
        flow_type    = 'service',
        workspace    = './log/',
        format       = LOGGING_FORMAT.STANDARD,
        handler_list = [LOGGING_HANDLER.STREAM, LOGGING_HANDLER.FILE],
        level        = LOGGING_LEVEL.DEBUG
    ):
        '''
        this is the constructor of the class Logger.

        parameters:
            - main_title <str>:
                the main title of the logger.

            - flow_type <str>:
                the service name of the logger.

            - workspace <str>:
                the directory of the logger file.

            - format <str>:
                the type of format is str, it descripts the format of the logging.

                for example:
                    '[%(asctime)s][%(name)12s][%(levelname)8s][%(message)s][%(pathname)s:%(lineno)d]'

            - handler_list <list>:
                the list of constructors of handlers.
                the default value is [STREAM, FILE].

            - level <int>:
                the minimum level of the logging.
                the default value is DEBUG.
        '''


        self.__logger = logging.getLogger(main_title)
        self.__logger.setLevel(LOGGING_LEVEL.DEBUG)

        file_name = os.path.join(workspace, '_'.join([main_title, flow_type])) + '_{:%Y%m%d}.log'.format(datetime.datetime.now())
        for handler in handler_list:
            self.__logger.addHandler(
                get_handler(
                    main_title = main_title,
                    handler    = handler,
                    level      = level,
                    format     = format,
                    file_name  = file_name
                )
            )

    def info(self, *args, **kwargs):
        '''
        provide the function info.

        parameters:
            it pass all input arguments into the function __logger.info.

        return:
            the result of __logger.info.
        '''

        return self.__logger.info(*args, **kwargs)

    def debug(self, *args, **kwargs):
        '''
        provide the function debug.

        parameters:
            it pass all input arguments into the function __logger.debug.

        return:
            the result of __logger.debug.
        '''

        return self.__logger.debug(*args, **kwargs)

    def warning(self, *args, **kwargs):
        '''
        provide the function warning.

        parameters:
            it pass all input arguments into the function __logger.warning.

        return:
            the result of __logger.warning.
        '''

        return self.__logger.warning(*args, **kwargs)

    def error(self, *args, **kwargs):
        '''
        provide the function error.

        parameters:
            it pass all input arguments into the function __logger.error.

        return:
            the result of __logger.error.
        '''

        return self.__logger.error(*args, **kwargs)

    def critical(self, *args, **kwargs):
        '''
        provide the function critical.

        parameters:
            it pass all input arguments into the function __logger.critical.

        return:
            the result of __logger.critical.
        '''

        return self.__logger.critical(*args, **kwargs)
