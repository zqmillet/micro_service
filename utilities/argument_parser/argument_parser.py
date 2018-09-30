import argparse
import textwrap
import colorama

class ArgumentParser(argparse.ArgumentParser):
    def __init__(self, *argv, **kwargs):
        super(ArgumentParser, self).__init__(formatter_class = argparse.RawTextHelpFormatter)

    def add_argument(self, *argv, **kwargs):
        if 'help' in kwargs:
            kwargs['help'] = kwargs['help'].strip().strip('.')
            comment_list = list()
            if 'type' in kwargs:
                comment_list.append('# parameter type: {type}'.format(type = kwargs['type']))
            if 'default' in kwargs and not kwargs['default'] == argparse.SUPPRESS:
                comment_list.append('# default value: {default}'.format(default = kwargs['default']))

            if len(comment_list) == 0:
                kwargs['help'] = '\n'.join(textwrap.wrap(kwargs['help']))
            else:
                kwargs['help'] = '\n'.join(textwrap.wrap(kwargs['help'])) + colorama.Fore.BLUE + '\n' + '\n'.join(comment_list) + colorama.Fore.RESET
        super(ArgumentParser, self).add_argument(*argv, **kwargs)
