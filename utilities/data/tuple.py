class Tuple(tuple):
    def __new__(self, *args, **kwargs):
        return super(Tuple, self).__new__(self, args)

    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self):
         return super(Tuple, self).__str__() + ', ' + str(self.__dict__)

def testcases():
    data = Tuple(1, 2, 3, x = 1, y = 2)
    print(data)

if __name__ == '__main__':
    testcases()
