from apscheduler.schedulers.background import BackgroundScheduler

class Scheduler:
    '''
    this class is used to manage the scheduled tasks.
    '''

    background_scheduler = None

    def __init__(self):
        '''
        this is the constructor of the class, and it has no paramete.
        '''

        self.background_scheduler = BackgroundScheduler()

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
            self.background_scheduler.add_job(function, **kwargs)
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

        self.background_scheduler.add_job(function, **kwargs)

    def start(self):
        '''
        this is the function to start the scheduler.
        '''

        self.background_scheduler.start()
