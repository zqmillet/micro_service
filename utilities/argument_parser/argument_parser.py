import argparse

class ArgumentParser(argparse.ArgumentParser):
    def add_argument(self, *argv, **kwargs):
        if 'help' in kwargs:
            if 'type' in kwargs:
                kwargs['help'] += ', parameter type {type}'.format(type = kwargs['type'])
            if 'default' in kwargs and not kwargs['default'] == '==SUPPRESS==':
                kwargs['help'] += ', default value: {default}'.format(default = kwargs['default'])
        super(ArgumentParser, self).add_argument(*argv, **kwargs)
