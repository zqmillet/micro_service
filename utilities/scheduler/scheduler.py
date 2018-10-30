import functools
import apscheduler.schedulers.background

from utilities.function_tools import Timer

class Scheduler:
    '''
    this class is used to manage the scheduled tasks.
    '''

    background_scheduler = None
    logger = None

    def __init__(self, logger):
        '''
        this is the constructor of the class, and it has no paramete.
        '''

        self.background_scheduler = apscheduler.schedulers.background.BackgroundScheduler()
        self.logger = logger

    def regist_task(self, **kwargs):
        '''
        this is a decorator, which can add the task into the scheduler.

        example:
            scheduler = Scheduler()
            @scheduler.regist_task(trigger = TRIGGER.CRON, second = '1,2,3,4,5')
            def print_time():
                print(time.ctime())
        '''

        def add_task(function):
            self.background_scheduler.add_job(self.bind_with_logger(function, **kwargs), **kwargs)
        return add_task

    def add_task(self, function, **kwargs):
        '''
        this is a function, which can add the task into the scheduler.

        example:
            def print_time():
                print(time.ctime())
            scheduler = Scheduler()
            scheduler.add_task(print_2333, trigger = TRIGGER.CRON, second = '6,7,8,9,10')
        '''

        self.background_scheduler.add_job(self.bind_with_logger(function, **kwargs), **kwargs)

    def bind_with_logger(self, function, **trigger):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            with Timer() as timer:
                result = function(*args, **kwargs)
            self.logger.info('the function {function_name} is called by trigger {trigger}, the time consuming is {time_consuming}s'.format(function_name = function.__qualname__, time_consuming = timer.interval, trigger = str(trigger)))
            return result
        return wrapper

    def start(self):
        '''
        this is the function to start the scheduler.
        '''

        self.background_scheduler.start()
