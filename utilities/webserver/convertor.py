import json
import numpy

def convert_to_string(data):
    if isinstance(data, numpy.ndarray):
        return json.dumps(data.tolist(), ensure_ascii = False, indent = 4)
    elif isinstance(data, list):
        return json.dumps(data, ensure_ascii = False, indent = 4)
