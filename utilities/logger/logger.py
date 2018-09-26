import os
import logging
import logging.config
import datetime

from utilities.logger import get_handler
from constants import LOGGING_LEVEL, LOGGING_HANDLER, LOGGING_FORMAT

class Logger:
    '''
    this class is used for logging.
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
            - main_title:
                the main title of the logger.

            - flow_type:
                the service name of the logger.

            - workspace:
                the directory of the logger file.

            - format:
                the type of format is str, it descripts the format of the logging.

                for example:
                    '[%(asctime)s][%(name)12s][%(levelname)8s][%(message)s][%(pathname)s:%(lineno)d]'

            - handler_list:
                the list of constructors of handlers.
                the default value is [STREAM, FILE].

            - level:
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
        return self.__logger.info(*args, **kwargs)

    def debug(self, *args, **kwargs):
        return self.__logger.debug(*args, **kwargs)

    def warning(self, *args, **kwargs):
        return self.__logger.warning(*args, **kwargs)

    def error(self, *args, **kwargs):
        return self.__logger.error(*args, **kwargs)

    def critical(self, *args, **kwargs):
        return self.__logger.critical(*args, **kwargs)
