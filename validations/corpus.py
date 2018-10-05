from utilities.system import iterate_files, iterate_lines
from constants import FILE_MODE, ENCODE

def main():
    file = open('./data/corpus/corpus_chs_20181004.txt', FILE_MODE.WRITE, encoding = ENCODE.UTF8)
    for file_path in iterate_files('./data/small_corpus/AA/'):
        for line in iterate_lines(file_path):
            line = line.strip()
            if line.startswith(r'<doc id='):
                continue
            if line.startswith(r'</doc>'):
                continue
            if line == '':
                continue

            file.write(line + '\n')

    file.close()


if __name__ == '__main__':
    main()
