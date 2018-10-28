import argparse
import textwrap
import colorama

class ArgumentParser(argparse.ArgumentParser):
    '''
    this class inherits from argparse.ArgumentParser.

    this class can show the types and default values of parameters, automatically.
    '''

    def __init__(self, *argv, **kwargs):
        '''
        this is the constructor of the class ArgumentParser.

        parameters:
            it will pass all import arguments into the function __init__ of class argparse.ArgumentParser.
        '''

        super(ArgumentParser, self).__init__(formatter_class = argparse.RawTextHelpFormatter)

    def add_argument(self, *argv, **kwargs):
        '''
        override the function add_argument.
        it will format the help messages of argument.

        parameters:
            it will pass all import arguments into the function __init__ of class argparse.ArgumentParser.
        '''

        if 'help' in kwargs:
            kwargs['help'] = kwargs['help'].strip().strip('.')
            break_line = '\n'
        else:
            kwargs['help'] = ''
            break_line = ''

        comment_list = list()
        if 'type' in kwargs:
            comment_list.append('# parameter type: {type}'.format(type = kwargs['type']))
        if 'default' in kwargs and not kwargs['default'] == argparse.SUPPRESS:
            comment_list.append('# default value: {default}'.format(default = kwargs['default']))

        comment = '' if len(comment_list) == 0 else colorama.Fore.BLUE + break_line + '\n'.join(comment_list) + colorama.Fore.RESET
        kwargs['help'] = '\n'.join(sum([textwrap.wrap(line) for line in kwargs['help'].split('\n')], [])) + comment
        super(ArgumentParser, self).add_argument(*argv, **kwargs)
