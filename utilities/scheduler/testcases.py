import time

from utilities.scheduler import Scheduler
from constants import TRIGGER

def testcases():
    scheduler = Scheduler()

    @scheduler.regist_task(trigger = TRIGGER.CRON, second = '1,2,3,4,5')
    def print_time():
        print(time.ctime())

    scheduler.start()

    while True:
        time.sleep(1)

if __name__ == '__main__':
    testcases()
