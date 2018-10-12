import json

from resources import word_vector

def get_word_vector(word):
    return json.dumps(word_vector[word].tolist(), indent = 4)
