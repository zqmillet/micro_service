import os
import re
import math

def iterate_files(directory, maximum_depth = 0, absolute_path = False, filter_pattern_list = None):
    '''
    this function is used to iterate all files in the directory.
    if the directory does not exist, it will not raise an error, but return nothing.

    parameters:
        - directory:
            this is the directory path.

        - maximum_depth:
            this is the maximum depth of iteration.
            the default value is 0, which means that all files will be iterated.

        - absolute_path:
            if absolute_path is True, return absolute path of each file;
            if absolute_path is False, return relative path of each file.
            the default is False.

        - filter_pattern_list:
            this is a list of regex patterns.
            if a file path matches one of filter_pattern_list, it will be ignored.
            the default value is empty list.

            for example:
                filter_pattern_list = [
                    re.compile(r'.*readme.*'),
                    re.compile('.*__.*'),
                    re.compile('.*\.git.*'),
                    re.compile('.*JSON$', flags = re.IGNORECASE)
                ]
    '''

    # initialize the maximum_depth.
    if maximum_depth <= 0:
        maximum_depth = math.inf

    # initialize the filter_pattern_list.
    if filter_pattern_list is None:
        filter_pattern_list = list()

    # iterate all files.
    for root, _, file_list in os.walk(directory):
        folder_list = [folder for folder in root[len(directory.strip(os.sep)):].split(os.sep) if not folder == '']
        if len(folder_list) >= maximum_depth:
            continue

        for file in file_list:
            file_path = os.path.join(root, file)

            if absolute_path:
                file_path = os.path.abspath(file_path)

            match_list = [pattern.match(file_path) for pattern in filter_pattern_list]
            if not [item for item in match_list if not item is None] == []:
                continue

            yield file_path

def testcases():
    filter_pattern_list = [
        re.compile(r'.*readme.*'),
        re.compile('.*__.*'),
        re.compile('.*\.git.*'),
        re.compile('.*JSON$', flags = re.IGNORECASE)
    ]

    for file_path in iterate_files('./', maximum_depth = 0, absolute_path = False, filter_pattern_list = filter_pattern_list):
        print(file_path)

    for file_path in iterate_files('./2333/'):
        print(file_list)

    help(iterate_files)

if __name__ == '__main__':
    testcases()
