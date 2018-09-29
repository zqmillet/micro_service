import gensim
import numpy

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
        '''
        the function __iter__ of the class CorpusGenerator must be overloaded.
        '''

        for file_path in iterate_files(self.directory):
            for line in iterate_lines(file_path):
                if self.word_splitter is None:
                    yield self.prefix + line.split() + self.suffix
                else:
                    yield self.prefix + self.word_splitter.split(line) + self.suffix

class WordVector(dict):
    '''
    this is a class to provide the training and searching of the word vector.

    member variables:
        - __black_dictionary:
            if an unknown word is queried twice, the return values should be same.
            this dictionary is used to record the random vectors of unknown words.

        - __shape:
            the shape of the word vector.

        - __random_generator:
            if an unknown word is queried, the WordVector will return a random vector,
            the __random_generator is used to generate this random vector.
    '''

    __black_dictionary = None
    __shape = None
    __random_generator = None

    def __init__(self, model_file_path = None, random_generator = None):
        '''
        this is the constructor of the class WordVector.

        parameters:
            - model_file_path:
                the path of the word embedding model file.
                if the model_file_path is None, it will not load the model from file.

            - random_generator:
                this is a generator which can generate random vector.
                the default random_generator is numpy.random.randn
        '''

        self.__random_generator = random_generator if not random_generator is None else numpy.random.randn

        if model_file_path is None:
            return

        model = gensim.models.Word2Vec.load(model_file_path)
        for word, information in model.wv.vocab.items():
            index = information.index
            self[word] = model.wv.syn0[index]
        self.__black_dictionary = dict()
        self.__shape = model.wv.syn0[0].shape

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

        '''
        this function is used to train a word vector from corpus.

        parameters:
            - corpus_generator:
                this is a CorpusGenerator.

            - algorithm:
                training algorithm: skip-gram or cbow.

            - vector_size:
                dimensionality of the word vectors.

            - alpha:
                the initial learning rate.

            - seed:
                seed for the random number generator, which is used to generate the initial value.

            - window_size:
                maximum distance between the current and predicted word within a sentence.

            - minimum_count:
                ignores all words with total frequency lower than this.

            - maximum_vocabulary_size:
                limits the RAM during vocabulary building.
                if there are more unique words than this, then prune the infrequent ones.
                every 10 million word types need about 1GB of RAM.
                set to None for no limit.

            - sample:
                the threshold for configuring which higher-frequency words are randomly downsampled, useful range is (0, 1e-5).

            - workers:
                use these many worker threads to train the model.

            - hierarchical_softmax:
                if True, hierarchical softmax will be used for model training.
                if False, and negative is non-zero, negative sampling will be used.

            - cbow_mean:
                 if 0, use the sum of the context word vectors.
                 if 1, use the mean, only applies when cbow is used.

            - iterations:
                number of iterations (epochs) over the corpus.

            - batch_words:
                target size (in words) for batches of examples passed to worker threads (and thus cython routines).
                larger batches will be passed if individual texts are longer than 10,000 words,
                but the standard cython code truncates to that maximum.
        '''

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
