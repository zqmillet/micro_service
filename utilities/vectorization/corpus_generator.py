from utilities.system import iterate_files, iterate_lines

class CorpusGenerator(object):
    '''
    this class is a generator which can iterate corpus in a directory.

    member variables:
        - word_splitter:
            this is a WordSplitter, which is used to split the chinese words.
            if word_splitter is None, the word will be splitted by space.

        - prefix:
            several placeholders at the begin of a line.

        - suffix:
            several placeholders at the end of a line.
    '''

    directory = None
    word_splitter = None
    prefix = None
    suffix = None

    def __init__(self, directory, window_size, placeholder, word_splitter = None):
        '''
        this is the constructor of the class CorpusGenerator.

        parameters:
            - directory:
                this is the directory in which there are corpus files.

            - window_size:
                this is the windows size of the ngram.
                if window_size = 3, the line will be expanded as:
                    [placeholder, placeholder, placeholder, word, word, ..., word, placeholder, placeholder, placeholder]

            - placeholder:
                the placeholder for the unknown words.

            - word_splitter:
                this is a WordSplitter, which is used to split the chinese words.
        '''

        self.directory = directory
        self.word_splitter = word_splitter
        self.prefix = [placeholder] * window_size
        self.suffix = [placeholder] * window_size

    def get_corpus_list(self):
        return list(iterate_files(self.directory, absolute_path = True))

    def __iter__(self):
        '''
        the function __iter__ of the class CorpusGenerator must be overloaded.
        '''

        for file_path in iterate_files(self.directory):
            for line in iterate_lines(file_path):
                if self.word_splitter is None:
                    yield self.prefix + line.split() + self.suffix
                else:
                    yield self.prefix + self.word_splitter.split(line) + self.suffix
