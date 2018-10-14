import json

from resources import word_vector
from utilities.webserver import convert_to_string

def get_word_vector(word) -> convert_to_string:
    return word_vector[word]

def testcases():
    print(get_word_vector('中国'))

if __name__ == '__main__':
    testcases()
