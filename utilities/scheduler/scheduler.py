from apscheduler.schedulers.background import BackgroundScheduler

class Scheduler:
    background_scheduler = None

    def __init__(self):
        self.background_scheduler = BackgroundScheduler()

    def regist_task(self, **kwargs):
        def add_task(function):
            self.background_scheduler.add_job(function, **kwargs)
        return add_task

    def start(self):
        self.background_scheduler.start()
