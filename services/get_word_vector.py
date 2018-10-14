import json

from resources import word_vector

def get_word_vector(word: str) -> lambda x: json.dumps(x.tolist(), indent = 4):
    return word_vector[word]

def testcases():
    print(get_word_vector('中国'))

if __name__ == '__main__':
    testcases()
