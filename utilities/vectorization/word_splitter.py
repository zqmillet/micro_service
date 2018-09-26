import jieba

from utilities.system import iterate_lines
from constants import FILE_MODE, ENCODE

class WordSplitter:
    dictionary = None
    tokenizer = None

    def __init__(self, dictionary_file_path = None):
        self.tokenizer = jieba.Tokenizer()
        self.dictionary = dict()
        if not dictionary_file_path is None:
            self.tokenizer.load_userdict(dictionary_file_path)
            for line in iterate_lines(dictionary_file_path):
                word = Word(line)
                self.dictionary[word.word] = word

        self.tokenizer.initialize()

    def split(self, text, format = 'list'):
        if format == 'list':
            format_function = lambda x: x
        else: # format == 'str'
            format_function = lambda x: ' '.join(x)

        return format_function(self.tokenizer.lcut(text))

    def export_dictionary(self, dictionary_file_path):
        with open(dictionary_file_path, FileMode.write, encoding = Encode.utf8) as file:
            for _, word in self.dictionary.items():
                file.write(word.to_string() + '\n')

class Word:
    word = None
    frequency = None
    part_of_speech = None

    def __init__(self, line):
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
        return ' '.join([str(item) for item in [self.word, self.frequency, self.part_of_speech] if not item is None])

def testcases():
    word_splitter = WordSplitter()
    print(word_splitter.split('李小福是创新办主任也是云计算方面的专家', format = 'string'))
    word_splitter = WordSplitter('./models/word_splitter.dict')
    print(word_splitter.split('李小福是创新办主任也是云计算方面的专家', format = 'list'))

if __name__ == '__main__':
    testcases()
