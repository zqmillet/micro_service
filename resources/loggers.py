from utilities.configuration import Configuration
from utilities.logger import Loggers
from utilities.function_tools import Timer

with Timer('<loggers> is loaded, the time consuming is {time}s') as timer:
    configuration = Configuration('./config/loggers.json')
    loggers = Loggers(configuration)
loggers.resources.info(timer.message)
