# import builtins
# import tqdm
# import os

# from constants import FILE_MODE, ENCODE

# def get_string_size(string):
#     return len(string.encode(ENCODE.UTF8))

# class File(object):
#     __file = None
#     __progress_bar = None
#     __size = None

#     def __init__(self, file_path, *args, **kwargs):
#         self.__file = builtins.open(file_path, *args, **kwargs)
#         self.__binary_file = builtins.open(file_path, FILE_MODE.BINARY_READ)
#         self.__size = os.path.getsize(file_path)
#         self.__progress_bar = tqdm.tqdm(total = self.__size)

#     def read(self):
#         size = self.__size // 100
#         data = ''
#         while True:
#             part = self.__binary_file.read(size)
#             data += part.decode(ENCODE.UTF8)
#             length = len(part)
#             self.__progress_bar.update(length)
#             if not length:
#                 break

#         return data

#     def __enter__(self):
#         return self

#     def __iter__(self):
#         for line in self.__file:
#             self.__progress_bar.update(get_string_size(line))
#             yield line

#     def __exit__(self, e_type, e_val, e_tb):
#         self.__file.close()
#         self.__file = None

# def open(file_path, *args, **kwargs):
#     return File(file_path, *args, **kwargs)

# def testcases():
#     from constants import FILE_MODE, ENCODE
#     with open('./data/corpus/wikipedia_chs_20180927.txt', FILE_MODE.READ, encoding = ENCODE.UTF8) as file:
#     # with open('./data/corpus/small.xml', FILE_MODE.READ, encoding = ENCODE.UTF8) as file:
#         print(file.read())


# if __name__ == '__main__':
#     testcases()
