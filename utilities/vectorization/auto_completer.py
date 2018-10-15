import numpy

from utilities.math import cosine_distance

class AutoCompleter(object):
    __candidate_list = None
    __word_vector    = None
    __text_matrix    = None
    __word_splitter  = None

    def __init__(self, candidate_list, word_vector, word_splitter):
        self.__candidate_list = candidate_list
        self.__word_vector    = word_vector
        self.__word_splitter  = word_splitter
        self.__text_matrix    = numpy.array([self.get_text_vector(candidate).tolist() for candidate in self.__candidate_list])

    def get_text_vector(self, text):
        return sum([self.__word_vector[word] for word in self.__word_splitter.split(text)])

    def auto_complete(self, text, topn = 10):
        text_vector = self.get_text_vector(text)
        distance_list = cosine_distance(self.__text_matrix, text_vector)
        nearest_index_list = distance_list.argsort()[:topn].tolist()
        return [{'text': self.__candidate_list[index], 'distance': distance_list[index]}  for index in nearest_index_list]

def testcases():
    import json

    from constants import FILE_MODE, ENCODE
    from utilities.configuration import Configuration
    from utilities.vectorization import WordVector, WordSplitter

    configuration = Configuration('./config/models.json')
    candidate_list = json.loads(open('./data/eason.json', FILE_MODE.READ, encoding = ENCODE.UTF8).read())
    word_vector = WordVector(configuration.word_vector)
    word_splitter = WordSplitter()
    auto_completer = AutoCompleter(candidate_list = candidate_list, word_vector = word_vector, word_splitter = word_splitter)

    print(auto_completer.auto_complete('疯狂革命'))

if __name__ == '__main__':
    testcases()
