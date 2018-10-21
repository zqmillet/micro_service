import collections

from utilities.function_tools import auto_type_checker

class Dictionary(collections.defaultdict):
    '''
    this class inherits from collections.defaultdict.

    this class override the function get of the collections.defaultdict.
    the function get will try all keys successively.
    '''

    @auto_type_checker
    def load(self, dictionary: (dict, collections.defaultdict)):
        '''
        this function is used to load the data from buildin dictionary.

        parameters:
            - dictionary:
                the buildin dictionary.
        '''

        for key, value in dictionary.items():
            if isinstance(value, dict) or isinstance(value, collections.defaultdict):
                self[key] = Dictionary()
                self[key].load(value)
            else:
                self[key] = value

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
