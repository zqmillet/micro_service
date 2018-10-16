from utilities.logger import Logger
from utilities.webserver import Server
from utilities.configuration import Configuration



def start():
    logger = Logger(
        main_title = 'webserver',
        flow_type = 'test'
    )
    configuration = Configuration('./config/services.json')
    server = Server(configuration = configuration, logger = logger, port = 8000)
    server.start()

if __name__ == '__main__':
    start()
