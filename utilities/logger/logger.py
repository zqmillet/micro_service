import os
import logging
import logging.config
import datetime

class LOGGING_LEVEL:
    INFO     = logging.INFO
    DEBUG    = logging.DEBUG
    WARNING  = logging.WARNING
    ERROR    = logging.ERROR
    CRITICAL = logging.CRITICAL
    NOTSET   = logging.NOTSET

class LOGGING_HANDLER:
    STREAM   = logging.StreamHandler
    FILE     = logging.handlers.TimedRotatingFileHandler

class LOGGING_FORMAT:
    '''
    %(asctime)s         - human-readable time when the LogRecord was created. by default this is of the form ‘2003-07-08 16:49:45,896’ (the numbers after the comma are millisecond portion of the time).
    %(created)f         - time when the LogRecord was created (as returned by time.time()).
    %(filename)s        - filename portion of pathname.
    %(funcName)s        - name of function containing the logging call.
    %(levelname)s       - text logging level for the message ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL').
    %(levelno)s         - numeric logging level for the message (DEBUG, INFO, WARNING, ERROR, CRITICAL).
    %(lineno)d          - source line number where the logging call was issued (if available).
    %(message)s         - the logged message, computed as msg % args. This is set when Formatter.format() is invoked.
    %(module)s          - module (name portion of filename).
    %(msecs)d           - millisecond portion of the time when the LogRecord was created.
    %(name)s            - name of the logger used to log the call.
    %(pathname)s        - full pathname of the source file where the logging call was issued (if available).
    %(process)d         - process id (if available).
    %(processName)s     - process name (if available).
    %(relativeCreated)d - time in milliseconds when the LogRecord was created, relative to the time the logging module was loaded.
    %(thread)d          - thread id (if available).
    %(threadName)s      - thread name (if available).
    '''

    STANDARD = '[%(asctime)s][%(name)12s][%(levelname)8s][%(message)s][%(pathname)s:%(lineno)d]'
    SIMPLE   = '[%(asctime)s][%(name)12s][%(levelname)8s][%(message)s][%(pathname)s:%(lineno)d]'

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

def get_3rd_party_log_filter(main_title):
    class Filter(logjing.Filter):
        def filter(self, record):
            return record.name == main_title
    return Filter()

def get_handler(main_title, handler, level, format, file_name):
    handler = handler(file_name) if handler == LOGGING_HANDLER.FILE else handler()

    handler.setLevel(level)
    formatter = logging.Formatter(format)
    handler.setFormatter(formatter)
    handler.addFilter(get_3rd_party_log_filter(main_title))
    return handler

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
