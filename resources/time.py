from utilities.function_tools import Timer
from utilities.system import Time

from resources.loggers import loggers

with Timer('<time> is loaded, the time consuming is {time}s') as timer:
    time = Time()

loggers.resources.info(timer.message)
