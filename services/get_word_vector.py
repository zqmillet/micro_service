from utilities.webserver import convert_to_string

from resources.word_vector import word_vector

def get_word_vector(word) -> convert_to_string:
    '''
    this function is used to get the word vector.

    parameters:
        - word <str>:
            the word.

    return <numpy.ndarray>:
        the word vector.
    '''

    return word_vector[word]

def testcases():
    print(get_word_vector('中国'))

if __name__ == '__main__':
    testcases()
