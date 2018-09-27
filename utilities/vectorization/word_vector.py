import gensim
import numpy
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from utilities.system import iterate_files, iterate_lines
from utilities.vectorization import WordSplitter

class CorpusGenerator(object):
    '''
    this class is a generator which can iterate corpus in a directory.

    member variables:
        - word_splitter:
            this is a WordSplitter, which is used to split the chinese words.
            if word_splitter is None, the word will be splitted by space.

        - prefix:
            several placeholders at the begin of a line.

        - suffix:
            several placeholders at the end of a line.
    '''

    word_splitter = None
    prefix = None
    suffix = None

    def __init__(self, directory, window_size, placeholder, word_splitter = None):
        '''
        this is the constructor of the class CorpusGenerator.

        parameters:
            - directory:
                this is the directory in which there are corpus files.

            - window_size:
                this is the windows size of the ngram.
                if window_size = 3, the line will be expanded as:
                    [placeholder, placeholder, placeholder, word, word, ..., word, placeholder, placeholder, placeholder]

            - placeholder:
                the placeholder for the unknown words.

            - word_splitter:
                this is a WordSplitter, which is used to split the chinese words.
        '''

        self.directory = directory
        self.word_splitter = word_splitter
        self.prefix = [placeholder] * window_size
        self.suffix = [placeholder] * window_size


    def __iter__(self):
        for file_path in iterate_files(self.directory):
            for line in iterate_lines(file_path):
                if self.word_splitter is None:
                    yield self.prefix + line.split() + self.suffix
                else:
                    yield self.prefix + self.word_splitter.split(line) + self.suffix

class WordVector(dict):
    __black_dictionary = None
    __shape = None
    __random_generator = None
    __model = None

    def __init__(self, model_file_path = None, random_generator = None):
        if model_file_path is None:
            return

        self.__model = gensim.models.Word2Vec.load(model_file_path)
        for word, information in self.__model.wv.vocab.items():
            index = information.index
            self[word] = self.__model.wv.syn0[index]
        self.__black_dictionary = dict()
        self.__shape = self.__model.wv.syn0[0].shape
        self.__random_generator = random_generator if not random_generator is None else numpy.random.randn

    def training(self,
                 corpus_generator,
                 algorithm               = 'cbow',
                 vector_size             = 128,
                 alpha                   = 0.025,
                 seed                    = 1,
                 window_size             = 5,
                 minimum_count           = 5,
                 maximum_vocabulary_size = None,
                 sample                  = 0.001,
                 workers                 = 4,
                 hierarchical_softmax    = True,
                 cbow_mean               = 1,
                 iterations              = 500,
                 batch_words             = 10000):

        self.model = gensim.models.Word2Vec(
            corpus_generator,
            size           = vector_size,
            alpha          = alpha,
            window         = window_size,
            min_count      = minimum_count,
            max_vocab_size = maximum_vocabulary_size,
            sample         = sample,
            seed           = seed,
            workers        = workers,
            sg             = 0 if algorithm == 'cbow' else 1,
            hs             = 1 if hierarchical_softmax == True else 0,
            cbow_mean      = cbow_mean,
            iter           = iterations,
            batch_words    = batch_words
        )

    def save(self, model_file_path):
        self.model.save(model_file_path)

    def __getitem__(self, word):
        if word in self:
            return self.get(word)

        if word in self.__black_dictionary:
            return self.__black_dictionary.get(word)

        vector = self.__random_generator(*self.__shape)
        self.__black_dictionary[word] = vector
        return vector

    def get_shape(self):
        return self.__shape

def testcases():
    corpus_generator = CorpusGenerator(
        directory = './data/corpus/',
        window_size = 5,
        placeholder = 'UNK',
        word_splitter = WordSplitter()
    )

    word_vector = WordVector()
    word_vector.training(corpus_generator)
    word_vector.save('./models/word_embedding.bin')

if __name__ == '__main__':
    testcases()
