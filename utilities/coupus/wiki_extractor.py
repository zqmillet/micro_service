from utilities.system import iterate_files, iterate_lines
from constants import FILE_MODE, ENCODE

def extract_corpus_from_wiki(directory, output_file_path):
    with open(output_file_path, FILE_MODE.WRITE, encoding = ENCODE.UTF8) as file:
        for file_path in iterate_files(directory):
            for line in iterate_lines(file_path, show_progress_bar = True):
                if line.startswith(r'</doc>'):
                    continue
                if line.startswith(r'<doc'):
                    continue
                if line.strip() == '':
                    continue
                file.write(line + '\n')

def testcases():
    extract_corpus_from_wiki('./data/corpus/AA', './data/corpus.txt')

if __name__ == '__main__':
    testcases()
