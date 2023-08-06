from numpy import ndarray
import numpy as np
from timeit import default_timer as timer
class CorankingException(Exception):
    def __init__(self, message, *args):
        super(CorankingException, self).__init__(message, *args)


class Coranking:
    def __init__(self):
        pass

    def run(self, HD: ndarray, LD: ndarray):
        try:
            if HD.size != LD.size:
                raise CorankingException("matrices hdpd and ldpd do not have the same sizes")

            nbr = HD.shape[0]
            sss = HD.shape[1]

            ndx1 = np.transpose(np.argsort(HD + 1, axis=1))
            ndx2 = np.transpose(np.argsort(LD + 1, axis=1))

            ndx1 = ndx1 + 1
            ndx2 = ndx2 + 1

            ndx4 = np.zeros((nbr + 1, sss + 1), dtype=np.uint32)
            start = timer()

            nbr_range = range(nbr)

            for j in range(sss):
                ndx4[ndx2[nbr_range, j], j] = nbr_range

            ndx4 = ndx4 + 1



            del ndx2

            c = np.zeros((nbr + 1, sss + 1), dtype=np.uint32)

            start = timer()

            for j in range(sss):
                h = ndx4[ndx1[nbr_range, j], j]
                c[nbr_range, h] = c[nbr_range, h] + 1


            del ndx1, ndx4

            c = np.delete(c, 0, axis=0)
            c = np.delete(c, 0, axis=1)
            c = np.delete(c, 0, axis=1)
            c = np.delete(c, -1, axis=0)
            return c

        except Exception as e:
            raise CorankingException(e)


