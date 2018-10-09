import time

from utilities.vectorization import WordVector

def testcases():
    word_vector = WordVector('./models/word_embedding.bin')

    for word in ['中国', '公司', '测试', '编程', '苹果']:
        now = time.time()
        print(word_vector.get_nearest_word_list(word, topn = 20))
        print(time.time() - now)

if __name__ == '__main__':
    testcases()
