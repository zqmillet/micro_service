import jieba

from utilities.system import iterate_lines
from constants import FILE_MODE, ENCODE

class WordSplitter:
    '''
    this class is used to split the chinese text.

    member variables:
        - __dictionary <dict>:
            the dictionary of word splitter.

        - __tokenizer <jieba.Tokenizer>:
            the tokenizer of jieba.
    '''

    __dictionary = None
    __tokenizer = None

    def __init__(self, dictionary_file_path = None):
        '''
        the constructor of the class WordSplitter.

        parameters:
            dictionary_file_path <str>:
                the path of the word splitter dictionary.

        return:
            nothing.
        '''

        self.__tokenizer = jieba.Tokenizer()
        self.__dictionary = dict()
        if not dictionary_file_path is None:
            self.__tokenizer.load_userdict(dictionary_file_path)
            for line in iterate_lines(dictionary_file_path):
                word = Word(line)
                self.__dictionary[word.word] = word

        self.__tokenizer.initialize()

    def split(self, text):
        '''
        this function is used to split the chinese text.

        parameters:
            - text <str>:
                the text to be splitted.

        return <[str, str, ..., str]>:
            a list of word.
        '''
        return self.__tokenizer.lcut(text)

    def export_dictionary(self, dictionary_file_path):
        '''
        this function is used to save the word split dictionary to the file.

        parameters:
            - dictionary_file_path <str>:
                the path of the word split dictionary.

        return:
            nothing.
        '''

        with open(dictionary_file_path, FILE_MODE.WRITE, encoding = ENCODE.UTF8) as file:
            for _, word in self.__dictionary.items():
                file.write(word.to_string() + '\n')

class Word:
    '''
    this class is the element of word split dictionary.

    member variables:
        - word <str>:
            the word.

        - frequency <int>:
            the frequency of the word.

        - part_of_speech <str>:
            the part of speech
    '''

    word = None
    frequency = None
    part_of_speech = None

    def __init__(self, line):
        '''
        this is the constructor of the class Word.

        parameters:
            - line <str>:
                the line of word split dictionary file.

                for example:
                    apple, 1, n
                    banana, n
                    sleep, 3
                    love

        return:
            nothing.
        '''

        line = line.split()

        self.word = line[0]
        if len(line) == 1:
            pass
        elif len(line) == 2:
            if line[1].isdigit():
                self.frequency = int(line[1])
            else:
                self.part_of_speech = line[1]
        else: # len(line) == 3:
            self.frequency = line[1]
            self.part_of_speech = line[2]

    def to_string(self):
        '''
        this function is used to convert the Word to string.

        parameters:
            nothing.

        return <str>:
            the line of word split dictionary file.
        '''

        return ' '.join([str(item) for item in [self.word, self.frequency, self.part_of_speech] if not item is None])

def testcases():
    word_splitter = WordSplitter()
    print(word_splitter.split('李小福是创新办主任也是云计算方面的专家'))
    word_splitter = WordSplitter('./models/word_splitter.dict')
    print(word_splitter.split('李小福是创新办主任也是云计算方面的专家'))

if __name__ == '__main__':
    testcases()
