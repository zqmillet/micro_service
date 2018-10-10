import collections

from exceptions import TypeError

class Dictionary(collections.defaultdict):
    def load(self, dictionary):
        for key, value in dictionary.items():
            if isinstance(value, dict) or isinstance(value, collections.defaultdict):
                self[key] = Dictionary()
                self[key].load(value)
            else:
                self[key] = value

    def get(self, argument, default_value = None):
        if isinstance(argument, str):
            if argument in self:
                return self[argument]
            else:
                return default_value
        elif isinstance(argument, list):
            for key in argument:
                if key in self:
                    return self[key]
            return default_value
        else:
            raise TypeError(type = type(argument))
