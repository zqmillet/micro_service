import functools
import inspect

from exceptions import InvalidValueError

def auto_type_checker(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        # fetch the argument name list.
        parameters = inspect.signature(function).parameters
        argument_name_list = list(parameters.keys())

        # fetch the argument checker list.
        checker_list = [parameters[argument_name].annotation for argument_name in argument_name_list]

        # fetch the value list.
        key_word_argument_name_list = argument_name_list[-len(kwargs)] if not len(kwargs) == 0 else list()
        value_list = list(args) + [kwargs[argument_name] for argument_name in key_word_argument_name_list]

        # initialize the result dictionary, where key is argument name, value is the checker result.
        result_dictionary = dict()
        for name, value, checker in zip(argument_name_list, value_list, checker_list):
            result_dictionary[name] = check(name, value, checker)


        # fetch the invalid argument name list.
        invalid_argument_name_list = [key for key in argument_name_list if not result_dictionary[key]]

        # if there are invalid arguments, raise the error.
        if len(invalid_argument_name_list) > 0:
            raise InvalidValueError(invalid_argument_name_list, function)

        # check the result.
        result = function(*args, **kwargs)
        checker = inspect.signature(function).return_annotation
        if not check('return', result, checker):
            raise InvalidValueError(['return'], function)

        # return the result.
        return result
    return wrapper

def check(name, value, checker):
    if isinstance(checker, (tuple, list, set)):

        return True in [check(name, value, sub_checker) for sub_checker in checker]
    elif checker is inspect._empty:
        return True
    elif isinstance(checker, type):
        return isinstance(value, checker)
    elif callable(checker):
        result = checker(value)
        if not isinstance(result, bool):
            print('the checker of {name} is invalid'.format(name = name))
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
        def add(self, a, b, c: [int, float], d: int) -> str:
            return self.base + a + b + c + d

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

if __name__ == '__main__':
    testcases()
