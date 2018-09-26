import os
import re
import math

def iterate_file(directory, maximum_depth = 0, absolute_path = False, filter_pattern_list = None):
    if maximum_depth <= 0:
        maximum_depth = math.inf

    if filter_pattern_list is None:
        filter_pattern_list = list()
    else:
        filter_pattern_list = [re.compile(regex) for regex in filter_pattern_list]

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

    for file_path in iterate_file('./', maximum_depth = 0, absolute_path = False, filter_pattern_list = filter_pattern_list):
        print(file_path)

if __name__ == '__main__':
    testcases()
