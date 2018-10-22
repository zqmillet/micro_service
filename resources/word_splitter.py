from utilities.vectorization import WordSplitter
from utilities.function_tools import Timer
from resources.loggers import loggers

with Timer('<word_splitter> is loaded, the time consuming is {time}s') as timer:
    word_splitter = WordSplitter()
loggers.resources.info(timer.message)
