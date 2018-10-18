import time

class Timer(object):
    interval = None
    message = None
    auto_print = None

    def __init__(self, message = None, auto_print = False):
        self.message = message
        self.auto_print = auto_print

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.end = time.time()
        self.interval = self.end - self.start
        if self.auto_print:
            self.message = self.message.format(time = self.interval)
            print(self.message)

def testcases():
    with Timer('consuming time is {time}s', auto_print = True):
        a = 3

    with Timer() as timer:
        a = sum(range(10000))

    print('consuming time is {time}s'.format(time = timer.interval))

if __name__ == '__main__':
    testcases()
