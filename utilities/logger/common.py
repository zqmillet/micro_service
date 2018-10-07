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
        # get the time that this sequence started at and make it a TimeTuple
        currentTime = int(time.time())
        dstNow = time.localtime(currentTime)[-1]
        t = self.rolloverAt - self.interval
        if self.utc:
            timeTuple = time.gmtime(t)
        else:
            timeTuple = time.localtime(t)
            dstThen = timeTuple[-1]
            if dstNow != dstThen:
                if dstNow:
                    addend = 3600
                else:
                    addend = -3600
                timeTuple = time.localtime(t + addend)
        suffix = self.get_time_string() + '.' + self.extension
        dfn = self.rotation_filename(self.baseFilename[:-len(suffix)] + suffix)

        if os.path.exists(dfn):
            os.remove(dfn)
        self.rotate(self.baseFilename, dfn)
        if self.backupCount > 0:
            for s in self.getFilesToDelete():
                os.remove(s)
        if not self.delay:
            self.stream = self._open()
        newRolloverAt = self.computeRollover(currentTime)
        while newRolloverAt <= currentTime:
            newRolloverAt = newRolloverAt + self.interval
        #If DST changes and midnight or weekly rollover, adjust for this.
        if (self.when == 'MIDNIGHT' or self.when.startswith('W')) and not self.utc:
            dstAtRollover = time.localtime(newRolloverAt)[-1]
            if dstNow != dstAtRollover:
                if not dstNow:  # DST kicks in before next rollover, so we need to deduct an hour
                    addend = -3600
                else:           # DST bows out before next rollover, so we need to add an hour
                    addend = 3600
                newRolloverAt += addend
        self.rolloverAt = newRolloverAt
