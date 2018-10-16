from utilities.webserver import convert_to_string
from resources import auto_completer

def auto_complete(text: str, topn: int = 10) -> convert_to_string:
    return auto_completer.auto_complete(text, topn)
