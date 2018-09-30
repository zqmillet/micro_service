import numpy
import json
import pickle
import uuid
import os

from utilities.vectorization import WordVector, CorpusGenerator, WordSplitter
from utilities.logger import Logger
from utilities.configuration import Configuration

def testcases():
    configuration = Configuration('./config/logging.json')
    logger = Logger(**configuration.word_vector_training)

    word_vector = WordVector()
    word_splitter = WordSplitter()

    window_size = 5
    corpus_generator = CorpusGenerator(
        './data/small_corpus',
        word_splitter = word_splitter,
        window_size = window_size,
        placeholder = 'UNK')

    model_file_path = './models/word_embedding.bin'

    word_vector.training(
        corpus_generator,
        logger = logger,
        iterations = 2,
        window_size = window_size
    )

    word_vector.save(model_file_path)
    word_vector = WordVector(model_file_path)

    print(json.dumps(word_vector.get_training_parameters(), ensure_ascii = False, indent = 4))
    # print(word_vector['文本'])
    # print(word_vector['这个词肯定不在词库里'])

    # os.remove(model_file_path)

    print(word_vector.get_nearest_word_list('中国'))

if __name__ == '__main__':
    testcases()
