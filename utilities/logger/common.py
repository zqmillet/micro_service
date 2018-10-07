import logging
import time
import datetime
import os

from constants import LOGGING_HANDLER

def get_3rd_party_log_filter(main_title):
    '''
    this function is used to generate a logging filter, which ignore all logs which has different main_title.

    parameters:
        - main_title <str>:
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
        - main_title <str>:
            this is the main title of the logging, which will be passed into the function get_3rd_party_log_filter.

        - handler <logging.Handler>:
            the constructor function of the handler.

            for example:
                - logging.StreamHandler
                - logging.handlers.TimedRotatingFileHandler

        - level <int>:
            the minimum level of the logging.

        - format <str>:
            the type of format is str, it descripts the format of the logging.

            for example:
                '[%(asctime)s][%(name)12s][%(levelname)8s][%(message)s][%(pathname)s:%(lineno)d]'

        - file_name <str>:
            this is the name of the log file.

    return <logging.Handler>:
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

class DailyFileHandler(logging.handlers.TimedRotatingFileHandler):
    def __init__(self, file_name, interval = 1, backup_count = 0, extension = 'log'):
       file_name = file_name + '_' + '0' * len(self.get_time_string()) + '.' + extension
       super(DailyFileHandler, self).__init__(
           filename    = file_name,
           when        = 'S',
           interval    = interval,
           backupCount = backup_count,
           encoding    = None,
           delay       = False,
           utc         = False,
           atTime      = None
       )
       self.extension = extension

    def get_time_string(self):
        return '{0:%Y%m%d%H%M%S}'.format(datetime.datetime.now())

    def doRollover(self):
        if self.stream:
            self.stream.close()
            self.stream = None

        current_time = int(time.time())
        time_now = time.localtime(current_time)[-1]

        suffix = self.get_time_string() + '.' + self.extension
        file_name = self.rotation_filename(self.baseFilename[:-len(suffix)] + suffix)

        if os.path.exists(file_name):
            os.remove(file_name)

        self.rotate(self.baseFilename, file_name)
        if self.backupCount > 0:
            for file_path in self.getFilesToDelete():
                os.remove(file_path)
        if not self.delay:
            self.stream = self._open()
        new_rollover_at = self.computeRollover(current_time)
        while new_rollover_at <= current_time:
            new_rollover_at = new_rollover_at + self.interval
        #If DST changes and midnight or weekly rollover, adjust for this.
        if (self.when == 'MIDNIGHT' or self.when.startswith('W')) and not self.utc:
            dstAtRollover = time.localtime(new_rollover_at)[-1]
            if time_now != dstAtRollover:
                if not time_now:  # DST kicks in before next rollover, so we need to deduct an hour
                    addend = -3600
                else:           # DST bows out before next rollover, so we need to add an hour
                    addend = 3600
                new_rollover_at += addend
        self.rolloverAt = new_rollover_at
