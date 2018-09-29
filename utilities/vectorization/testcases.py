import numpy
import json
import pickle
import uuid
import os

from utilities.vectorization import WordVector, CorpusGenerator, WordSplitter

def testcases():
    word_vector = WordVector()
    word_splitter = WordSplitter()

    window_size = 5
    corpus_generator = CorpusGenerator(
        './data/small_corpus',
        word_splitter = word_splitter,
        window_size = window_size,
        placeholder = 'UNK')

    model_file_path = './models/' + str(uuid.uuid1()) + '.bin'

    word_vector.training(
        corpus_generator,
        iterations = 20,
        window_size = window_size
    )

    word_vector.save(model_file_path)
    word_vector = WordVector(model_file_path)

    print(json.dumps(word_vector.get_training_parameters(), ensure_ascii = False, indent = 4))
    print(word_vector['文本'])
    print(word_vector['这个词肯定不在词库里'])

    os.remove(model_file_path)

if __name__ == '__main__':
    testcases()
