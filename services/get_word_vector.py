import json

from resources import word_vector

def get_word_vector(word):
    return json.dumps(word_vector[word].tolist(), indent = 4)

def testcases():
    print(get_word_vector('中国'))

if __name__ == '__main__':
    testcases()
