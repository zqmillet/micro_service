import gensim
import numpy
import pickle
import json

from utilities.vectorization import WordSplitter, CorpusGenerator
from constants import FILE_MODE

class WordVector:
    '''
    this is a class to provide the training and searching of the word vector.

    member variables:
        - __black_dictionary:
            if an unknown word is queried twice, the return values should be same.
            this dictionary is used to record the random vectors of unknown words.

        - __shape:
            the shape of the word vector.

        - __training_parameters:
            a dictionary to record the training paramenter.
    '''

    __black_dictionary = None
    __shape = None
    __training_parameters = None
    __matrix = None
    __word_index_dictionary = None

    def __init__(self, model_file_path = None):
        '''
        this is the constructor of the class WordVector.

        parameters:
            - model_file_path:
                the path of the word embedding model file.
                if the model_file_path is None, it will not load the model from file.
        '''

        if model_file_path is None:
            return

        self.load_from_pickle(model_file_path)

    def training(self,
                 corpus_generator,
                 logger                  = None,
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
                 iterations              = 10,
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

        self.__training_parameters = {
            'corpus_list'            : corpus_generator.get_corpus_list(),
            'algorithm'              : algorithm,
            'vector_size'            : vector_size,
            'alpha'                  : alpha,
            'seed'                   : seed,
            'window_size'            : window_size,
            'minimum_count'          : minimum_count,
            'maximum_vocabulary_size': maximum_vocabulary_size,
            'sample'                 : sample,
            'workers'                : workers,
            'hierarchical_softmax'   : hierarchical_softmax,
            'cbow_mean'              : cbow_mean,
            'iterations'             : iterations,
            'batch_words'            : batch_words
        }

        if not logger is None:
            gensim.models.word2vec.logger = logger
            gensim.models.base_any2vec.logger = logger

        model = gensim.models.Word2Vec(
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
        self.load_from_gensim_model(model)

    def load_from_gensim_model(self, gensim_model):
        self.__word_index_dictionary = {word: information.index for word, information in gensim_model.wv.vocab.items()}
        self.__matrix = gensim_model.wv.syn0
        self.__black_dictionary = dict()
        self.__shape = gensim_model.wv.syn0[0].shape

    def load_from_pickle(self, model_file_path):
        with open(model_file_path, FILE_MODE.BINARY_READ) as file:
            word_vector = pickle.load(file)
            self.__dict__ = word_vector.__dict__

    def get_training_parameters(self):
        return self.__training_parameters

    def save(self, model_file_path):
        with open(model_file_path, FILE_MODE.BINARY_WRITE) as file:
            file.write(pickle.dumps(self))

    def __getitem__(self, word):
        if word in self.__word_index_dictionary:
            return self.__matrix[self.__word_index_dictionary[word]]

        if word in self.__black_dictionary:
            return self.__black_dictionary.get(word)

        vector = numpy.random.randn(*self.__shape)
        self.__black_dictionary[word] = vector
        return vector

    def get_shape(self):
        return self.__shape
