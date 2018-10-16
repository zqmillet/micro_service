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
        '-t', '--title',
        action   = 'store',
        type     = str,
        default  = 'micro_service',
        help     = 'specify the main title for the logger'
    )
    arguments.add_argument(
        '-f', '--flow',
        action   = 'store',
        type     = str,
        default  = 'casebot',
        help     = 'specify the flow type for the logger'
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

    logger = Logger(
        main_title = arguments.title,
        flow_type  = arguments.flow
    )
    configuration = Configuration(arguments.configuration)
    server = Server(configuration = configuration, logger = logger, port = arguments.port)
    server.start()

if __name__ == '__main__':
    start()
