from utilities.logger import Logger
from utilities.configuration import Configuration
from utilities.function_tools import auto_type_checker
from constants import LOGGING_FORMAT

class Loggers(dict):
    @auto_type_checker
    def __init__(self, configuration: Configuration):
        maximum_width = 0
        for key, value in configuration.items():
            width = len(value.main_title + '.' + value.flow_type)
            if width > maximum_width:
                maximum_width = width

        for key, value in configuration.items():
            logger = Logger(format = LOGGING_FORMAT.MONONAME_STANDARD.format(width = maximum_width), **value)
            self[key] = logger
            setattr(self, key, logger)

def testcases():
    configuration = Configuration('./config/loggers.json')
    loggers = Loggers(configuration)

    loggers.main.info('23333')
    loggers.word_vector.info('this is test')

if __name__ == '__main__':
    testcases()
