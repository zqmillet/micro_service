import logging.handlers
import datetime
import time
import os

from utilities.function_tools import auto_type_checker

class DailyFileHandler(logging.handlers.TimedRotatingFileHandler):
    '''
    this class inherits from the class logging.handlers.TimedRotatingFileHandler.

    this class overrides functions __init__ and doRollover of the class logging.handlers.TimedRotatingFileHandler.
    '''

    @auto_type_checker
    def __init__(self, file_name: str, interval: int = 1, backup_count: int = 0, extension: str = 'log'):
        '''
        this fucntion is the constructor of the class DailyFileHandler.

        parameters:
            - file_name:
                the name of the logging file.

            - interval:
                how many days between two logging files.

            - backup_count:
                how many logging files are used to backup.

            - extension:
                the extension of the logging files.
        '''

        file_name = file_name + '.' + '0' * len(self.get_yesterday_string()) + '.' + extension
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

    @auto_type_checker
    def get_yesterday_string(self) -> str:
        '''
        this function is used to get the yesterday date string.
        '''

        return '{0:%Y%m%d}'.format(datetime.datetime.now() - datetime.timedelta(1))

    def doRollover(self):
        '''
        this function is used to override the doRollover function of the class logging.handlers.TimedRotatingFileHandler.
        '''

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
