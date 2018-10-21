import inspect

def get_function_value_list(function, *args, **kwargs):
    specification = inspect.getfullargspec(function)

    # print('input args: ', args)
    # print('input kwargs: ', kwargs)
    # print('function default: ',specification.defaults)
    # print('function args: ', specification.args)

    value_list = list()
    for index, argument in enumerate(specification.args):
        if index < len(args):
            value_list.append(args[index])
            continue

        if argument in kwargs:
            value_list.append(kwargs[argument])
            continue

        value_list.append(specification.defaults[index - len(specification.args) + len(specification.defaults)])
    return value_list

def testcases():
    def function(aa, bb, cc, dd = 'dd', ee = 'ee', ff = 'ff'):
        pass

    print(get_function_value_list(function, 'a', 'b', cc = 'c', ff = 'f'))

if __name__ == '__main__':
    testcases()
