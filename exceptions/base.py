import colorama

class BaseException(Exception):
    message = None

    def __str__(self):
        return colorama.Fore.RED + self.__class__.__name__ + ': ' + colorama.Fore.RESET + self.message.format(**{key: value for key, value in self.__dict__.items() if not key == 'message'})
