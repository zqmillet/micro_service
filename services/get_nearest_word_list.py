from resources import word_vector

def get_nearest_word_list(word, topn = 10):
    return word_vector.get_nearest_word_list(word, topn)
