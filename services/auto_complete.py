import json

from resources import word_vector
from utilities.vectorization import WordSplitter, AutoCompleter
from utilities.webserver import convert_to_string
from constants import FILE_MODE, ENCODE

candidate_list = json.load(open('./data/eason.json', FILE_MODE.READ, encoding = ENCODE.UTF8))
word_splitter = WordSplitter()

auto_completer = AutoCompleter(candidate_list = candidate_list, word_vector = word_vector, word_splitter = word_splitter)

def auto_complete(text: str, topn: int = 10) -> convert_to_string:
    return auto_completer.auto_complete(text, topn)
