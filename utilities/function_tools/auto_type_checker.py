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

        argument_dictionary = dict()
        for name, value, checker in zip(argument_name_list, value_list, checker_list):

        result = function(*args, **kwargs)
        return
    return wrapper

def testcases():
    @auto_type_convertor
    def add(a, b, c: int, d: int = 3) -> str:
        return a + b + c + d

    @auto_type_convertor
    def cat(x: lambda x: str(x).strip(), y: lambda x: str(x).strip()) -> lambda x: '"' + str(x) + '"':
        return x + y

    print(add(1, 2, '3'))
    print(add(1, 2, '3', '4'))

    print(cat('text   ', '   text'))
    print(cat(1234, 4567))

if __name__ == '__main__':
    testcases()
