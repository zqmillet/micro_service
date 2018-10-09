from utilities.singleton import Singleton

def testcases():
    singleton_1 = Singleton()
    singleton_2 = Singleton()
    print(singleton_1 is singleton_2)

    class Test:
        pass

    test_1 = Test()
    test_2 = Test()
    print(test_1 is test_2)

    class Test(Singleton):
        pass

    test_1 = Test()
    test_2 = Test()
    print(test_1 is test_2)

if __name__ == '__main__':
    testcases()
