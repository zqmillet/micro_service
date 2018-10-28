import sys

from utilities.argument_parser import ArgumentParser

def testcases():
    argument_parser = ArgumentParser()

    argument_parser.add_argument(
        '-c', '--configuration',
        type = str,
        action = 'store',
        help = 'specify the configuration file path'
    )
    argument_parser.add_argument(
        '-p', '--port',
        type = int,
        action = 'store',
        default = 8000,
        help = 'specify the port'
    )
    argument_parser.add_argument(
        '-o', '--output',
        type = str,
        action = 'store',
        default = './'
    )

    argument_parser.parse_args(sys.argv[1:])

if __name__ == '__main__':
    testcases()
