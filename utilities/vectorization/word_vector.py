import gensim
import numpy
import pickle
import json

from utilities.vectorization import WordSplitter, CorpusGenerator
from utilities.math import cosine_distance
from constants import FILE_MODE

class WordVector:
    '''
    this is a class to provide the training and searching of the word vector.

    member variables:
        - __black_dictionary <dict>:
            if an unknown word is queried twice, the return values should be same.
            this dictionary is used to record the random vectors of unknown words.

        - __shape <tuple>:
            the shape of the word vector.

        - __training_parameters <dict>:
            a dictionary to record the training paramenter.

        - __matrix <numpy.ndarray>:
            the array of word vector.

        - __word_index_dictionary <dict>:
            a dictionary, where key is word, and value is index.

        - __index_word_dictionary <dict>:
            a dictionary, where key is index, and value is word.
    '''

    __black_dictionary = None
    __shape = None
    __training_parameters = None
    __matrix = None
    __word_index_dictionary = None
    __index_word_dictionary = None

    def __init__(self, model_file_path = None):
        '''
        this is the constructor of the class WordVector.

        parameters:
            - model_file_path <str>:
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
            - corpus_generator <CorpusGenerator>:
                this is a corpus generator.

            - algorithm <str>:
                training algorithm: skip-gram or cbow.

            - vector_size <int>:
                dimensionality of the word vectors.

            - alpha <float>:
                the initial learning rate.

            - seed <int>:
                seed for the random number generator, which is used to generate the initial value.

            - window_size <int>:
                maximum distance between the current and predicted word within a sentence.

            - minimum_count <int>:
                ignores all words with total frequency lower than this.

            - maximum_vocabulary_size <int>:
                limits the RAM during vocabulary building.
                if there are more unique words than this, then prune the infrequent ones.
                every 10 million word types need about 1GB of RAM.
                set to None for no limit.

            - sample <float>:
                the threshold for configuring which higher-frequency words are randomly downsampled, useful range is (0, 1e-5).

            - workers <int>:
                use these many worker threads to train the model.

            - hierarchical_softmax <bool>:
                if True, hierarchical softmax will be used for model training.
                if False, and negative is non-zero, negative sampling will be used.

            - cbow_mean <int>:
                 if 0, use the sum of the context word vectors.
                 if 1, use the mean, only applies when cbow is used.

            - iterations <int>:
                number of iterations (epochs) over the corpus.

            - batch_words <int>:
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
        '''
        this function is used to initialize all member variables from the model trained by gensim.

        parameters:
            - gensim_model <gensim.models.word2vec.Word2Vec>:
                the model generate by gensim.
        '''

        self.__word_index_dictionary = {word: information.index for word, information in gensim_model.wv.vocab.items()}
        self.__index_word_dictionary = {information.index: word for word, information in gensim_model.wv.vocab.items()}

        self.__matrix = gensim_model.wv.syn0
        self.__black_dictionary = dict()
        self.__shape = gensim_model.wv.syn0[0].shape

    def load_from_pickle(self, model_file_path):
        '''
        this function is used to initialize all member variables from the model generated by itself.

        parameters:
            - model_file_path <str>:
                the path of the model file.
        '''

        with open(model_file_path, FILE_MODE.BINARY_READ) as file:
            word_vector = pickle.load(file)
            self.__dict__ = word_vector.__dict__

    def get_training_parameters(self):
        '''
        this function is used to fetch the training parameters of the word vector.

        paramters:
            nothing.
        '''

        return self.__training_parameters

    def save(self, model_file_path):
        '''
        this function is used to save itself to the file.

        parameters:
            - model_file_path <str>:
                the path of the model file.
        '''

        with open(model_file_path, FILE_MODE.BINARY_WRITE) as file:
            file.write(pickle.dumps(self))

    def get_nearest_word_list(self, word, topn = 10):
        '''
        this function is used to get the nearest topn synonyms of a word in euclidean space.

        parameters:
            - word <str>:
                the word.

            - topn <int>:
                the number of results.
        '''

        word_vector = self[word]
        distance_list = cosine_distance(self.__matrix, word_vector)
        nearest_index_list = distance_list.argsort()[:topn]
        result = [{'word':self.__index_word_dictionary[index], 'distance':distance_list[index]} for index in nearest_index_list]
        return result

    def __getitem__(self, word):
        '''
        this function is used to override the function __getitem__.

        if the word is in the self.__word_index_dictionary, return the word vector.
        if the word is not in the self.__word_index_dictionary, return a random word vector.

        parameters:
            - word <str>:
                the word.
        '''

        if word in self.__word_index_dictionary:
            return self.__matrix[self.__word_index_dictionary[word]]

        if word in self.__black_dictionary:
            return self.__black_dictionary.get(word)

        vector = numpy.random.randn(*self.__shape)
        self.__black_dictionary[word] = vector
        return vector

    def get_shape(self):
        '''
        this function is used to get the shape of the word vector.

        parameters:
            nothing.
        '''

        return self.__shape
