import logging
import logging.config

class Logger:
    __logger = None

    def __init__(self, name, level):
        self.__logger = logging.getLogger(name)
        self.__logger.setLevel(level)

    def info(self, *args, **kwargs):
        return self.__logger.info(*args, **kwargs)

    def debug(self, *args, **kwargs):
        return self.__logger.debug(args, **kwargs)

    def warning(self, *args, **kwargs):
        return self.__logger.warning(*args, **kwargs)

    def error(self, *args, **kwargs):
        return self.__logger.error(*args, **kwargs)

    def critical(self, *args, **kwargs):
        return self.__logger.critical(*args, **kwargs)

def testcases():
    logger = Logger('test')
    logger.info('this is info')
    logger.debug('this is debug')
    logger.warning('this is warning')
    logger.error('this is error')
    logger.critical('this is critical')

if __name__ == '__main__':
    testcases()
