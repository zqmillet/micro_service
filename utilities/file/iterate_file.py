import os
import re
import math

def iterate_file(directory, maximum_depth = 0, absolute_path = False, filter_regex = ''):
    if maximum_depth <= 0:
        maximum_depth = math.inf

    for root, _, file_list in os.walk(directory):
        folder_list = [folder for folder in root[len(directory.strip(os.sep)):].split(os.sep) if not folder == '']
        if len(folder_list) >= maximum_depth:
            continue

        for file in file_list:
            file_path = os.path.join(root, file)
            if absolute_path:
                file_path = os.path.abspath(file_path)

            yield file_path

def testcases():
    for file_path in iterate_file('./', maximum_depth = 2, absolute_path = False):
        print(file_path)

if __name__ == '__main__':
    testcases()
