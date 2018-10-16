import json

from utilities.vectorization import AutoCompleter
from resources import word_vector, word_splitter
from constants import FILE_MODE, ENCODE

auto_completer = AutoCompleter(
    candidate_list = json.load(open('./data/eason.json', FILE_MODE.READ, encoding = ENCODE.UTF8)),
    word_vector    = word_vector,
    word_splitter  = word_splitter
)
