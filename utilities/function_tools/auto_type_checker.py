import functools
import inspect

def auto_type_convertor(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        parameters = inspect.signature(function).parameters
        argument_name_list = list(parameters.keys())
        checker_list = [parameters[argument_name].annotation for argument_name in argument_name_list]
        key_word_argument_name_list = argument_name_list[-len(kwargs)] if not len(kwargs) == 0 else list()
        value_list = list(args) + [kwargs[argument_name] for argument_name in key_word_argument_name_list]

        result_dictionary = dict()
        for name, value, checker in zip(argument_name_list, value_list, checker_list):
            result_dictionary[name] = check(name, value, checker)

        result = function(*args, **kwargs)
        checker = inspect.signature(function).return_annotation
        result_dictionary['return'] = check('return', result, checker)
        invalid_argument_name_list = [key for key, value in result_dictionary.items() if not value]
        if len(invalid_argument_name_list) > 0:
            print(
                '{names} are/is invalid, please see the file {file_name}, line number {line_number}'.format(
                    names = ', '.join(invalid_argument_name_list),
                    file_name = function.__code__.co_filename,
                    line_number = function.__code__.co_firstlineno
                )
            )
        return result
    return wrapper

def check(name, value, checker):
    if checker is inspect._empty:
        return True
    elif isinstance(checker, type):
        return isinstance(value, checker)
    elif callable(checker):
        result = checker(value)
        if not isinstance(result, bool):
            print('the checker of {name} is invalid'.format(name = name))
        return result

def testcases():
    @auto_type_convertor
    def add(a, b, c: int, d: int = 3) -> str:
        return int(a) + int(b) + int(c) + int(d)

    @auto_type_convertor
    def cat(x: lambda x: x > 0, y: int) -> bool:
        return (x + y) > 3

    print(add(1, 2, '3'))
    print(add(1, 2, '3', '4'))

    print(cat(1, 3))
    print(cat(-1, 3))

if __name__ == '__main__':
    testcases()
