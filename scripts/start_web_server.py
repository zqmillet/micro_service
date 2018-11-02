import sys

from utilities.argument_parser import ArgumentParser
from utilities.logger import Logger
from utilities.webserver import Server
from utilities.configuration import Configuration

def parse_arguments():
    arguments = ArgumentParser()
    arguments.add_argument(
        '-c', '--configuration',
        action   = 'store',
        type     = str,
        required = True,
        help     = 'specify the service configuration file path'
    )
    arguments.add_argument(
        '-p', '--port',
        action   = 'store',
        type     = int,
        default  = 8000,
        help     = 'specify the listening port of the server'
    )

    return arguments.parse_args(sys.argv[1:])

def start():
    arguments = parse_arguments()

    from resources.loggers import loggers
    configuration = Configuration(arguments.configuration)
    server = Server(configuration = configuration, logger = loggers.main, port = arguments.port)
    server.start()

if __name__ == '__main__':
    start()
