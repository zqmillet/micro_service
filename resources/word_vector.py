from utilities.vectorization import WordVector
from utilities.configuration import Configuration
from utilities.function_tools import Timer
from resources import loggers

with Timer('<word_vector> is loaded, the time consuming is {time}s') as timer:
    configuration = Configuration('./config/models.json')
    word_vector = WordVector(configuration.word_vector)
loggers.resources.info(timer.message)
