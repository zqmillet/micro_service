import numpy
import pickle

from utilities.vectorization import WordVector, CorpusGenerator, WordSplitter

def testcases():
    word_vector = WordVector()
    word_vector.load_from_pickle('./models/word_embedding.pkl')
    # word_vector.save('./models/word_embedding.pkl')

if __name__ == '__main__':
    testcases()
