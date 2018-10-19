import json

from utilities.vectorization import AutoCompleter
from utilities.function_tools import Timer
from resources import word_vector, word_splitter, loggers
from constants import FILE_MODE, ENCODE

with Timer('<auto_completer> is loaded, the time consuming is {time}s') as timer:
    auto_completer = AutoCompleter(
        candidate_list = json.load(open('./data/eason.json', FILE_MODE.READ, encoding = ENCODE.UTF8)),
        word_vector    = word_vector,
        word_splitter  = word_splitter
    )
loggers.resources.info(timer.message)
