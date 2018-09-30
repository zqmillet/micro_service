import argparse
import sys

from utilities.vectorization import WordVector, CorpusGenerator, WordSplitter
from utilities.logger import Logger

def parse_argument():
    arguments = argparse.ArgumentParser()
    arguments.add_argument(
        '-d', '--corpus_directory',
        action = 'store',
        type = str,
        required = True,
        help = 'specify the corpus directory'
    )
    arguments.add_argument(
        '-o', '--output',
        action = 'store',
        type = str,
        required = True,
        help = 'output of the word vector model'
    )
    arguments.add_argument(
        '-t', '--title',
        action = 'store',
        type = str,
        default = 'micro_service',
        help = 'set the title of the log file'
    )
    arguments.add_argument(
        '-f', '--flow',
        action = 'store',
        type = str,
        default = 'word_vector_training',
        help = 'set the flow type of the log file'
    )
    arguments.add_argument(
        '-u', '--word_dictionary',
        action = 'store',
        type = str,
        default = None,
        help = 'specify the directory of the word splitter'
    )
    arguments.add_argument(
        '-a', '--algorithm',
        action = 'store',
        type = str,
        default = 'cbow',
        help = 'training algorithm: skip-gram or cbow'
    )
    arguments.add_argument(
        '-l', '--vector_size',
        action = 'store',
        type = int,
        default = 128,
        help = 'dimensionality of the word vectors'
    )
    arguments.add_argument(
        '-r', '--alpha',
        action = 'store',
        type = float,
        default = 0.025,
        help = 'the initial learning rate'
    )
    arguments.add_argument(
        '-s', '--seed',
        action = 'store',
        type = int,
        default = 1,
        help = 'seed for the random number generator, which is used to generate the initial value'
    )
    arguments.add_argument(
        '-w', '--window_size',
        action = 'store',
        type = int,
        default = 5,
        help = 'maximum distance between the current and predicted word within a sentence'
    )
    arguments.add_argument(
        '-c', '--minimum_count',
        action = 'store',
        type = int,
        default = 5,
        help = 'ignores all words with total frequency lower than this'
    )
    arguments.add_argument(
        '-v', '--maximum_vocabulary_size',
        action = 'store',
        type = int,
        default = None,
        help = 'limits the RAM during vocabulary building. if there are more unique words than this, then prune the infrequent ones. every 10 million word types need about 1GB of RAM. set to -1 for no limit.'
    )
    arguments.add_argument(
        '-p', '--sample',
        action = 'store',
        type = float,
        default = 0.001,
        help = 'the threshold for configuring which higher-frequency words are randomly downsampled, useful range is (0, 1e-5)'
    )
    arguments.add_argument(
        '-j', '--workers',
        action = 'store',
        type = int,
        default = 4,
        help = 'use these many worker threads to train the model'
    )
    arguments.add_argument(
        '-x', '--hierarchical_softmax',
        action = 'store',
        type = bool,
        default = True,
        help = 'if True, hierarchical softmax will be used for model training. if False, and negative is non-zero, negative sampling will be used'
    )
    arguments.add_argument(
        '-m', '--cbow_mean',
        action = 'store',
        type = int,
        default = 1,
        help = 'if 0, use the sum of the context word vectors. if 1, use the mean, only applies when cbow is used'
    )
    arguments.add_argument(
        '-i', '--iterations',
        action = 'store',
        type = int,
        default = 20,
        help = 'number of iterations (epochs) over the corpus'
    )
    arguments.add_argument(
        '-b', '--batch_words',
        action = 'store',
        type = int,
        default = 10000,
        help = 'target size (in words) for batches of examples passed to worker threads (and thus cython routines). larger batches will be passed if individual texts are longer than 10,000 words, but the standard cython code truncates to that maximum'
    )
    arguments.add_argument(
        '-k', '--placeholder',
        action = 'store',
        type = str,
        default = 'UNK',
        help = 'the placeholder for the unknown words'
    )

    return arguments.parse_args(sys.argv[1:])

def main():
    # parse the input arguments.
    arguments = parse_argument()

    # initialize the word splitter.
    word_splitter = WordSplitter(arguments.word_dictionary)

    # initialize the corpus generator.
    corpus_generator = CorpusGenerator(
        directory     = arguments.corpus_directory,
        word_splitter = word_splitter,
        window_size   = arguments.window_size,
        placeholder   = arguments.placeholder
    )

    # create a logger.
    logger = Logger(
        main_title    = arguments.title,
        flow_type     = arguments.flow
    )

    # the follows are not training parameters.
    non_training_parameter_list = [
        'corpus_directory',
        'output',
        'title',
        'flow',
        'word_dictionary',
        'placeholder'
    ]

    # extract the training parameters.
    training_parameters = {key: value for key, value in arguments.__dict__.items() if not key in non_training_parameter_list}

    # create a word vector.
    word_vector = WordVector()

    # start the training.
    word_vector.training(
        corpus_generator = corpus_generator,
        logger           = logger,
        **training_parameters
    )

    # save the model.
    word_vector.save(arguments.output)

if __name__ == '__main__':
    main()

