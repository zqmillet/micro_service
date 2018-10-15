class AutoCompleter(object):
    __candidate_list = None
    __word_vector = None
    __text_matrix = None

    def __init__(self, candidate_list, word_vector):
        self.__candidate_list = candidate_list
        self.__word_vector = word_vector

    def get_text_vector(self, text):
        pass

def testcases():
    import json

    from constants import FILE_MODE, ENCODE
    from utilities.configuration import Configuration
    from utilities.vectorization import WordVector

    configuration = Configuration('./config/models.json')
    candidate_list = json.loads(open('./data/eason.json', FILE_MODE.READ, encoding = ENCODE.UTF8).read())
    word_vector = WordVector(configuration.word_vector)
    auto_completer = AutoCompleter(candidate_list = candidate_list, word_vector = word_vector)

if __name__ == '__main__':
    testcases()
