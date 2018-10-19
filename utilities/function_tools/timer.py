import time

class Timer(object):
    interval = None
    message = None
    auto_print = None

    def __init__(self, message = None, auto_print = False):
        self.message = message if not message is None else 'consuming time is {time}s'
        self.auto_print = auto_print

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.end = time.time()
        self.interval = self.end - self.start
        self.message = self.message.format(time = self.interval)
        if self.auto_print:
            print(self.message)

def testcases():
    with Timer(auto_print = True):
        a = 3

    with Timer('2333 {time} 2333') as timer:
        a = sum(range(100000))

    print(timer.message)

if __name__ == '__main__':
    testcases()
