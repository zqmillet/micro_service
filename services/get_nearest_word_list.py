import json

from resources import word_vector

def get_nearest_word_list(word, topn = '10'):
    topn = int(topn)
    return json.dumps(word_vector.get_nearest_word_list(word, topn), ensure_ascii = False, indent = 4)

def testcases():
    print(get_nearest_word_list('中国', topn = '3'))

if __name__ == '__main__':
    testcases()
