import logging

from constants import LOGGING_HANDLER

def get_3rd_party_log_filter(main_title):
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

def get_handler(main_title, handler, level, format, file_name):
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

    handler = handler(file_name) if handler == LOGGING_HANDLER.FILE else handler()
    handler.setLevel(level)
    formatter = logging.Formatter(format)
    handler.setFormatter(formatter)
    handler.addFilter(get_3rd_party_log_filter(main_title))
    return handler
