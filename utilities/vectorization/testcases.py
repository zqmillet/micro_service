import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from utilities.vectorization import WordVector, CorpusGenerator, WordSplitter

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
