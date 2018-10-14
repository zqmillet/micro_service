import json
import numpy

def convert_to_string(data):
    '''
    this function is used to convert the input data into the string.

    parameters:
        - data <any>:
            the input data.

    return <string>:
        the converted data.
    '''

    if isinstance(data, numpy.ndarray):
        return json.dumps(data.tolist(), ensure_ascii = False, indent = 4)
    elif isinstance(data, list):
        return json.dumps(data, ensure_ascii = False, indent = 4)
