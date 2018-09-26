import os
import tqdm

from constants import ENCODE, FILE_MODE

def get_string_size(string):
    return len(string.encode(ENCODE.UTF8))

def iterate_lines(file_path, encoding = ENCODE.UTF8, show_progress_bar = False):
    '''
    this function is used to iterate lines of text file.
    if the file does not exist, this function will not raise an error, but return nothing.

    parameters:
        - file_path:
            this is the path of the file which will be iterated.

        - encoding:
            specify the encoding of the file.
            the default value is utf8.

        - show_progress_bar:
            if show_progress_bar is True, a progress bar is shown.
            the default value is False.
    '''

    if not os.path.isfile(file_path):
        return

    file_size = os.path.getsize(file_path)
    progress_bar = tqdm.tqdm(total = file_size) if show_progress_bar else None

    with open(file_path, FILE_MODE.READ, encoding = encoding) as file:
        for line in file:
            if show_progress_bar:
                progress_bar.update(get_string_size(line))
            yield line.strip('\n')

def testcases():
    for line in iterate_lines('./config/database.json', show_progress_bar = False):
        print(line)

    for line in iterate_lines('./file_which_does_not_exist'):
        print(line)

    help(iterate_lines)

if __name__ == '__main__':
    testcases()
