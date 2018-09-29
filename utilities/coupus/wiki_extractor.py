import xml.etree.ElementTree
import re
import io

from utilities.system import iterate_lines

import builtins


class File(object):
    """A basic file-like object."""

    def __init__(self, path, *args, **kwargs):
        self._file = builtins.open(path, *args, **kwargs)

    def read(self, n_bytes = -1):
        data = self._file.read(n_bytes)
        print(233)
        return data

    def __enter__(self):
        return self

    def __exit__(self, e_type, e_val, e_tb):
        self._file.close()
        self._file = None

def open(path, *args, **kwargs):
    return File(path, *args, **kwargs)

def get_tag(element):
    m = re.match('\{.*\}', element.tag)
    return m.group(0) if m else ''

def testcases():
    with open('./data/corpus/small.xml', 'r', encoding = 'utf8') as file:
        iterparse = xml.etree.ElementTree.iterparse(file, events = ('start', 'end'))
        print(iterparse.root)
        for event, element in iterparse:
            if event == 'end':
                if get_tag(element) == 'page':
                    print(''.join(element.itertext()))

if __name__ == '__main__':
    testcases()

