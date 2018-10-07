import logging
import logging.config

class LOGGING_LEVEL:
    INFO     = logging.INFO
    DEBUG    = logging.DEBUG
    WARNING  = logging.WARNING
    ERROR    = logging.ERROR
    CRITICAL = logging.CRITICAL
    NOTSET   = logging.NOTSET

class LOGGING_HANDLER:
    STREAM   = 'STREAM' # logging.StreamHandler
    FILE     = 'FILE' # logging.handlers.TimedRotatingFileHandler

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
