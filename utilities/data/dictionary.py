import collections

from utilities.function_tools import auto_type_checker

class Dictionary(collections.defaultdict):
    '''
    this class inherits from collections.defaultdict.

    this class override the function get of the collections.defaultdict.
    the function get will try all keys successively.
    '''

    def get(self, argument, default_value = None):
        '''
        this function is used to overrided the function get of the class dict or collections.defaultdict.

        parameters:
            - argument <list>/<str>/...:
                if the type of argument is list, it will be regarded as a list of keys, and the function will try all keys successively.
                if the type of argument is not list, will be regarded as a key.

            - default_value <any>:
                if all keys are not in this dictionary, this function will return the default_value.
        '''

        if isinstance(argument, list):
            for key in argument:
                if key in self:
                    return self[key]
            return default_value
        else:
            if argument in self:
                return self[argument]
            else:
                return default_value

def testcases():
    dictionary = Dictionary()
    dictionary['name'] = 'qiqi'
    dictionary['age'] = '18'

    print(dictionary.get('name'))
    print(dictionary.get(['alias', 'hahaha', 'name']))

if __name__ == '__main__':
    testcases()
