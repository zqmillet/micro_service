from utilities.webserver import convert_to_string
from resources import word_splitter

def word_split(text: str, format: str = 'list') -> convert_to_string:
    if format == 'list':
        return word_splitter.split(text)
    else:
        return ' '.join(word_splitter.split(text))
