from utilities.webserver import Application
from utilities.logger import Logger

def start(configuration):
    logger = Logger(
        main_title = 'test',
        flow_type = 'application'
    )
    application = Application(logger = logger)

    for service_name in configuration.keys():
        service_information = getattr(configuration, service_name)
        application.regist_service(
            function = getattr(configuration, service_name).function,
            api_path = service_information.api_path,
            method_list = service_information.method_list.split('/')
        )
    application.start(port = 8000)

if __name__ == '__main__':
    from utilities.configuration import Configuration
    start(Configuration('./config/services.json'))
