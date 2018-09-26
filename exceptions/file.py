from exceptions import BaseException

class FileDoesNotExistError(BaseException):
    file_path = None
    message = 'the file "{file_path}" does not exist.'

    def __init__(self, file_path):
        self.file_path = file_path

class DirectoryDoesNotExistError(BaseException):
    directory_path = None
    message = 'the directory "{directory_path}" does not exist.'

    def __init__(self, directory_path):
        self.directory_path = directory_path
