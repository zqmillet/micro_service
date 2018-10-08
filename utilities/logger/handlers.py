import logging.handlers
import datetime
import time
import os

class DailyFileHandler(logging.handlers.TimedRotatingFileHandler):
    def __init__(self, file_name, interval = 1, backup_count = 0, extension = 'log'):
       file_name = file_name + '_' + '0' * len(self.get_yesterday_string()) + '.' + extension
       super(DailyFileHandler, self).__init__(
           filename    = file_name,
           when        = 'MIDNIGHT',
           interval    = interval,
           backupCount = backup_count,
           encoding    = None,
           delay       = False,
           utc         = False,
           atTime      = None
       )
       self.extension = extension

    def get_yesterday_string(self):
        return '{0:%Y%m%d}'.format(datetime.datetime.now() - datetime.timedelta(1))

    def doRollover(self):
        if self.stream:
            self.stream.close()
            self.stream = None

        current_time = int(time.time())
        time_now = time.localtime(current_time)[-1]

        suffix = self.get_yesterday_string() + '.' + self.extension
        file_name = self.rotation_filename(self.baseFilename[:-len(suffix)] + suffix)

        if os.path.exists(file_name):
            os.remove(file_name)

        self.rotate(self.baseFilename, file_name)
        if self.backupCount > 0:
            for file_path in self.getFilesToDelete():
                os.remove(file_path)

        self.stream = self._open()
        self.rolloverAt = self.computeRollover(current_time)
