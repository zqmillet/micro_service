import logging

from constants import LOGGING_HANDLER
from utilities.logger import DailyFileHandler
from utilities.function_tools import auto_type_checker

@auto_type_checker
def get_3rd_party_log_filter(main_title: str):
    '''
    this function is used to generate a logging filter, which ignore all logs which has different main_title.

    parameters:
        - main_title:
            this filter only remains the logs whose main title is equal to main_title.
    '''

    class Filter(logging.Filter):
        def filter(self, record):
            return record.name == main_title
    return Filter()

@auto_type_checker
def get_handler(main_title: str, handler: str, level: int, format: str, file_name: str) -> logging.Handler:
    '''
    this function is used to generate a logging handler.

    parameters:
        - main_title:
            this is the main title of the logging, which will be passed into the function get_3rd_party_log_filter.

        - handler:
            the constructor function of the handler.

            for example:
                - logging.StreamHandler
                - logging.handlers.TimedRotatingFileHandler

        - level:
            the minimum level of the logging.

        - format:
            the type of format is str, it descripts the format of the logging.

            for example:
                '[%(asctime)s][%(name)12s][%(levelname)8s][%(message)s][%(pathname)s:%(lineno)d]'

        - file_name:
            this is the name of the log file.

    return:
        the handler of logging.
    '''

    if handler == LOGGING_HANDLER.FILE:
        handler = DailyFileHandler(file_name)
    else:
        handler = logging.StreamHandler()

    handler.setLevel(level)
    formatter = logging.Formatter(format)
    handler.setFormatter(formatter)
    handler.addFilter(get_3rd_party_log_filter(main_title))
    return handler
