import logging

from constants import LOGGING_HANDLER

def get_3rd_party_log_filter(main_title):
    class Filter(logging.Filter):
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
