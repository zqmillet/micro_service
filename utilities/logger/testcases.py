from utilities.logger import Logger

def testcases():
    import logging
    import time

    logger1 = Logger(
        main_title = 'testcasebot',
        flow_type = 'mr'
    )

    # logger2 = Logger(
    #     main_title = 'testdatabot',
    #     flow_type = 'ml'
    # )

    import pdb; pdb.set_trace()
    logger1.info('this is info.')
    logger1.debug('this is debug.')
    logger1.warning('this is warning.')
    logger1.error('this is error.')
    logger1.critical('this is critical.')

    # logger2.info('this is info.')
    # logger2.debug('this is debug.')
    # logger2.warning('this is warning.')
    # logger2.error('this is error.')
    # logger2.critical('this is critical.')

    for index in range(333):
        time.sleep(1)
        logger1.info('text' + str(index))

    logging.info('this message should not be printed.')

if __name__ == '__main__':
    testcases()
