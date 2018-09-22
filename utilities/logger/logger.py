import os
import logging
import logging.config
import datetime

from utilities.logger import get_handler
from constants import LOGGING_LEVEL, LOGGING_HANDLER, LOGGING_FORMAT

class Logger:
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

def testcases():
    logger1 = Logger(
        main_title = 'testcasebot',
        flow_type = 'mr'
    )

    logger2 = Logger(
        main_title = 'testdatabot',
        flow_type = 'ml'
    )

    logger1.info('this is info.')
    logger1.debug('this is debug.')
    logger1.warning('this is warning.')
    logger1.error('this is error.')
    logger1.critical('this is critical.')

    logger2.info('this is info.')
    logger2.debug('this is debug.')
    logger2.warning('this is warning.')
    logger2.error('this is error.')
    logger2.critical('this is critical.')

    logging.info('this message should not be printed.')

if __name__ == '__main__':
    testcases()
