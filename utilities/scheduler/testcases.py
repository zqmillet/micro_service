import time

from utilities.scheduler import Scheduler
from constants import TRIGGER

def testcases():
    # initialize a scheduler.
    scheduler = Scheduler()

    # add a task by the decorator regist_task.
    @scheduler.regist_task(trigger = TRIGGER.CRON, second = '1,2,3,4,5')
    def print_time():
        print(time.ctime())

    # add a task by the function add_task.
    scheduler.add_task(lambda: print(time.ctime()), trigger = TRIGGER.CRON, second = '6,7,8,9,10')

    # start the scheduler.
    scheduler.start()

    # hold on.
    while True:
        time.sleep(1)

if __name__ == '__main__':
    testcases()
