from utilities.dictionary import Dictionary

def testcases():
    buildin_dictionary = {
        'a': 'a',
        'b': 'b',
        'c': {
            '1': 1,
            '2': 2
        }
    }

    dictionary = Dictionary()
    dictionary.load(buildin_dictionary)
    print(dictionary)

    print(dictionary.get('a'))
    print(dictionary.get(['d', 'e'], 3))
    print(dictionary.get(['d', 'e', 'a'], 3))

if __name__ == '__main__':
    testcases()
