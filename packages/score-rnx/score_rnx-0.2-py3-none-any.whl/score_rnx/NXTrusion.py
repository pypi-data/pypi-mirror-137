import numpy as np

class NX_TrusionException(Exception):
    def __init__(self, message, *args):
        super(NX_TrusionException, self).__init__(message, *args)


class NXTrusion:
    def __init__(self):
        pass

    def run(self, C: np.ndarray):

        try:
            size = C.shape
            print(size)
            if size[0] != size[1]:
                return
            nmo = size[0]
            sss = np.sum(C, axis=1)
            sss = sss[0]

            v1 = np.arange(1, nmo + 1)
            v2 = np.dot(sss, v1)

            n = np.zeros(nmo)

            x = np.zeros(nmo)

            p = np.cumsum(np.diag(C)) / v2

            b = v1 / nmo

            v3 = []

            for k in range(1, nmo):
                v3.append(k - 1)
                n[k] = np.sum(C[k, v3])
                x[k] = np.sum(C[v3, k])

            n = np.cumsum(n) / v2
            x = np.cumsum(x) / v2

            return [n, x, p, b]

        except Exception as e:
            raise NX_TrusionException(e)