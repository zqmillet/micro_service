import os
import logging
import datetime

from utilities.logger import get_handler
from constants import LOGGING_LEVEL, LOGGING_HANDLER, LOGGING_FORMAT

class Logger(logging.Logger):
    '''
    this class is used for logging.

    member variables:
        nothing.
    '''

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
            - main_title <str>:
                the main title of the logger.

            - flow_type <str>:
                the service name of the logger.

            - workspace <str>:
                the directory of the logger file.

            - format <str>:
                the type of format is str, it descripts the format of the logging.

                for example:
                    '[%(asctime)s][%(name)12s][%(levelname)8s][%(message)s][%(pathname)s:%(lineno)d]'

            - handler_list <list>:
                the list of constructors of handlers.
                the default value is [STREAM, FILE].

            - level <int>:
                the minimum level of the logging.
                the default value is DEBUG.
        '''

        main_title += '.' + flow_type
        logger = logging.getLogger(main_title)
        self.__dict__ = logger.__dict__
        self.setLevel(LOGGING_LEVEL.DEBUG)
        self.propagate = False

        file_name = os.path.join(workspace, '_'.join([main_title, flow_type])).format(datetime.datetime.now())
        for handler in handler_list:
            self.addHandler(
                get_handler(
                    main_title = main_title,
                    handler    = handler,
                    level      = level,
                    format     = format,
                    file_name  = file_name
                )
            )
