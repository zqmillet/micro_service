import gensim
import numpy

from utilities.system import iterate_files, iterate_lines
from utilities.vectorization import WordSplitter

class CorpusGenerator(object):
    word_splitter = None
    placeholder = None
    window_size = None

    def __init__(self, directory, window_size, placeholder, word_splitter = None):
        self.directory = directory
        self.word_splitter = word_splitter
        self.placeholder = placeholder
        self.window_size = window_size

    def __iter__(self):
        prefix = [self.placeholder] * self.window_size
        suffix = [self.placeholder] * self.window_size
        for file_path in iterate_files(self.directory):
            for line in iterate_lines(file_path):
                if self.word_splitter is None:
                    yield prefix + line.split() + suffix
                else:
                    yield prefix + self.word_splitter.split(line) + suffix

class WordVector(dict):
    __black_dictionary = None
    __shape = None
    __random_generator = None
    __model = None

    def __init__(self, model_file_path = None, random_generator = None):
        if model_file_path is None:
            pass

        self.__model = gensim.models.Word2Vec.load(model_file_path)
        for word, information in self.__model.wv.vocab.items():
            index = information.index
            self[word] = self.__model.wv.syn0[index]
        self.__black_dictionary = dict()
        self.__shape = self.__model.wv.syn0[0].shape
        self.__random_generator = random_generator if not random_generator is None else numpy.random.randn

    def training(self,
                 corpus_directory,
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
                 iterations              = 100,
                 batch_words             = 10000):

        self.model = gensim.models.Word2Vec(
            Corpus(directory),
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
        pass

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
    # word_vector = WordVector('./models/word_embedding.bin')
    # print(word_vector['关掉'])
    # print(word_vector['hfdsjkhfsjdkhjsdfhsdhf'])
    # print(word_vector.get_shape())

    corpus_generator = CorpusGenerator(
        './data/corpus/',
        window_size = 5,
        placeholder = 'UNK',
        word_splitter = WordSplitter()
    )

    for sample in corpus_generator:
        print(sample)
        import pdb; pdb.set_trace()

if __name__ == '__main__':
    testcases()
