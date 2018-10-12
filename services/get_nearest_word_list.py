import json

from resources import word_vector

def get_nearest_word_list(word, topn = 10):
    return json.dumps(word_vector.get_nearest_word_list(word, topn), ensure_ascii = False, indent = 4)
