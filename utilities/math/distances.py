import numpy
import scipy.spatial

def cosine_distance(matrix, vector):
    '''
    this function is used calculate the cosine distance'

    parameters:
        - matrix <numpy.ndarray>:
            the list of <numpy.array>, whose dimension is same to parameter vector.

            for example:
                maxtrix = [
                    [1, 1],
                    [1, 0],
                    [0, 1]
                ]

        - vector <numpy.array>/<list>:
            the vector.

            for example:
                vector = [1, 1]

    return <numpy.array>:
        the list of cosine distance.

        for example:
            maxtrix = [
                [1, 1],
                [1, 0],
                [0, 1]
            ]
            vector = [1, 1]

            result
            = cosine_distance(matrix, vector)
            = [
                1,
                0.7071067811865476,
                0.7071067811865476
            ]
    '''

    if isinstance(vector, list):
        vector = numpy.array(vector)
    vector = vector.reshape(1, -1)
    return scipy.spatial.distance.cdist(matrix, vector, 'cosine').reshape(-1)
