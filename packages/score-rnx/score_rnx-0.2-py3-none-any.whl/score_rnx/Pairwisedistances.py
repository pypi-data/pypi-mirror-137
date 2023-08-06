import numpy as np

class PairwisedistancesException(Exception):
    def __init__(self, message, *args):
        super(PairwisedistancesException, self).__init__(message, *args)


class Pairwisedistances:
    def __init__(self):
        pass

    def run(self, X: np.ndarray):
        X = np.array(X, dtype=np.float64)

        g = np.dot(X, np.transpose(X))

        di = np.diag(g)

        d = np.transpose(np.subtract(di, g))

        matrix_squared = (d + np.transpose(d))

        try:

            result = np.sqrt(abs(matrix_squared))

            return result
        except Exception as e:
            raise  Pairwisedistances(e)
