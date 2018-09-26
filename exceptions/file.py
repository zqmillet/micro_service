class FileDoesNotExistError(Exception):
    file_path = None

    def __init__(self, file_path):
        self.file_path = file_path

    def __str__(self):
        return 'the file {file_path} does not exist.'.format(file_path = self.file_path)

class DirectoryDoesNotExistError(Exception):
    directory_path = None

    def __init__(self, directory_path):
        self.directory_path = directory_path

    def __str__(self):
        return 'the directory {directory_path} does not exist.'.format(directory_path = self.directory_path)
