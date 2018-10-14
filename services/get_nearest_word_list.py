import json

from resources import word_vector

def get_nearest_word_list(word: str, topn: int = 10) -> lambda x: json.dumps(x, ensure_ascii = False, indent = 4):
    '''
    this function is used to get the nearest word list of the input word.

    parameters:
        - word <str>:
            the input word.

        - topn <int>:
            the element number of the nearest word list.

    return <list>:
        the nearest word list
    '''

    return word_vector.get_nearest_word_list(word, topn)

def testcases():
    print(get_nearest_word_list('中国', topn = 3))

if __name__ == '__main__':
    testcases()
