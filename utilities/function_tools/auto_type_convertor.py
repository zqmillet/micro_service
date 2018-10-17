import functools
import inspect

def auto_type_convertor(function):
    '''
    because, the input arguments from the requests package are all string,
    this function is used to auto convert the input arguments of the function according to the function.__annotations__.

    for example:
        @convert_input_argument_type
        def add(x: int, y: int) -> str:
            return x + y

        the result of the code add(3, y = '2') is '5'.
    '''

    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        parameters = inspect.signature(function).parameters
        argument_keys = tuple(parameters.keys())

        argument_list = list()
        for index, argument in enumerate(args):
            annotation = parameters[argument_keys[index]].annotation
            annotation = annotation if callable(annotation) else lambda x: x
            argument_list.append(annotation(argument))

        argument_dictionary = dict()
        for argument in kwargs:
            argument_dictionary[argument] = function.__annotations__.get(argument, lambda x: x)(kwargs[argument])

        return function.__annotations__.get('return', lambda x: x)(function(*argument_list, **argument_dictionary))
    return wrapper

def testcases():
    @auto_type_convertor
    def add(x: int, y: int) -> str:
        return x + y

    @auto_type_convertor
    def cat(x: lambda x: str(x).strip(), y: lambda x: str(x).strip()) -> lambda x: '"' + str(x) + '"':
        return x + y

    print(add(3, '2'))
    print(add(3, y = '2'))

    print(cat('text   ', '   text'))
    print(cat(1234, 4567))

if __name__ == '__main__':
    testcases()
