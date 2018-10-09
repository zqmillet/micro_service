from utilities.vectorization import WordVector
from utilities.configuration import Configuration

configuration = Configuration('./config/models.json')
word_vector = WordVector(configuration.word_vector)
