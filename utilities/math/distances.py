import numpy
import scipy.spatial

def cosine_distance(matrix, vector):
    if isinstance(vector, list):
        vector = numpy.array(vector)
    vector = vector.reshape(1, -1)
    return scipy.spatial.distance.cdist(matrix, vector, 'cosine').reshape(-1)
