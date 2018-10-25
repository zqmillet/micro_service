import collections

def is_none(x):
    return x is None

def is_hashable(x):
    return isinstance(x, collections.Hashable)
