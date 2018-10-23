import functools
import inspect

def auto_type_convertor(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        parameters = inspect.signature(function).parameters
        argument_name_list = list(parameters.keys())
        convertor_list = [parameters[argument_name].annotation for argument_name in argument_name_list]
        key_word_argument_name_list = argument_name_list[-len(kwargs)] if not len(kwargs) == 0 else list()
        value_list = list(args) + [kwargs[argument_name] for argument_name in key_word_argument_name_list]

        argument_dictionary = dict()
        for name, value, convertor in zip(argument_name_list, value_list, convertor_list):
            argument_dictionary[name] = convertor(value) if not convertor is inspect._empty else value

        convertor = inspect.signature(function).return_annotation
        result = function(**argument_dictionary)
        return convertor(result) if not convertor is inspect._empty else result
    return wrapper

def testcases():
    @auto_type_convertor
    def add(a, b, c: int, d: int = 3):
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