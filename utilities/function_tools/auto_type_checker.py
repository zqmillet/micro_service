import functools
import inspect

from exceptions import InvalidValueError, InvalidCheckerError

def auto_type_checker(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        # fetch the argument name list.
        parameters = inspect.signature(function).parameters
        argument_list = list(parameters.keys())

        # fetch the argument checker list.
        checker_list = [parameters[argument].annotation for argument in argument_list]

        # fetch the value list.
        value_list =  [inspect.getcallargs(function, *args, **kwargs)[argument] for argument in inspect.getfullargspec(function).args]

        # initialize the result dictionary, where key is argument, value is the checker result.
        result_dictionary = dict()
        for argument, value, checker in zip(argument_list, value_list, checker_list):
            result_dictionary[argument] = check(argument, value, checker, function)

        # fetch the invalid argument list.
        invalid_argument_list = [key for key in argument_list if not result_dictionary[key]]

        # if there are invalid arguments, raise the error.
        if len(invalid_argument_list) > 0:
            raise InvalidValueError(invalid_argument_list, function)

        # check the result.
        result = function(*args, **kwargs)
        checker = inspect.signature(function).return_annotation
        if not check('return', result, checker, function):
            raise InvalidValueError(['return'], function)

        # return the result.
        return result
    return wrapper

def check(name, value, checker, function):
    if isinstance(checker, (tuple, list, set)):
        return True in [check(name, value, sub_checker, function) for sub_checker in checker]
    elif checker is inspect._empty:
        return True
    elif checker is None:
        return value is None
    elif isinstance(checker, type):
        return isinstance(value, checker)
    elif callable(checker):
        result = checker(value)
        if not isinstance(result, bool):
            raise InvalidCheckerError(name, function)
        return result

def testcases():
    @auto_type_checker
    def add(a, b, c: (int, float), d: int) -> str:
        return a + b + c + d

    @auto_type_checker
    def test(x: lambda x: x >= 0, y: list, z: str) -> str:
        return y[x] == z

    class Test():
        base = 1
        @auto_type_checker
        def add(self, a, b, c: [int, float], d: int) -> lambda x: str(x):
            return self.base + a + b + c + d

    @auto_type_checker
    def test3(x: int, y: (None, int) = None):
        if y is None:
            y = 0
        return x + y

    try:
        print(add(1, 2, 2.3, 3.4))
    except Exception as e:
        print(e)

    try:
        print(test(-2, 3, 4))
    except Exception as e:
        print(e)

    try:
        print(test(2, [1, 2, 3, 4], '3'))
    except Exception as e:
        print(e)

    var = Test()
    try:
        var.add(1, 2, 3.3, 4.5)
    except Exception as e:
        print(e)

    try:
        var.add(1, 2, 3, 4)
    except Exception as e:
        print(e)

    print(test3(3))
    print(test3(4, 4))

if __name__ == '__main__':
    testcases()
