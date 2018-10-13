from utilities.webserver import Application

def start(service_configuration, logger, port):
    application = Application(logger = logger)

    for service_name in service_configuration.keys():
        service_information = getattr(service_configuration, service_name)
        if not service_information.enable:
            continue
        application.regist_service(
            function    = getattr(service_configuration, service_name).function,
            api_path    = service_information.api_path,
            method_list = service_information.methods.split('/')
        )
    application.start(port = port)
