from numpy import ndarray
import numpy as np
from typing import Any
from score_rnx.Pairwisedistances import Pairwisedistances
from score_rnx.Coranking import Coranking
from score_rnx.NXTrusion import NXTrusion

class ScoreRnx:
    def __init__(self, data: ndarray, method: ndarray) -> None:
        self.__data = data
        self.__method = method
        self.__score = 0
        self.__curve = Any

        self.pairwisedistances = Pairwisedistances()
        self.coranking = Coranking()
        self.nx_trusion = NXTrusion()

    def run(self):

        try:

            [Ravg, R_NX] = self.nx_scores(self.__data, self.__method)
            self.__score = Ravg
            self.__curve = R_NX

        except Exception as e:
            print(e)
                # lanzar una excepcion

    def get_rnx(self):
        return [self.__score, self.__curve]

    def nx_scores(self, HD: np.ndarray, LD: np.ndarray):
        try:

            nbr = len(HD)

                # Crear matrices de distancias para datos en alta y baja dimension


            DX = self.pairwisedistances.run(HD)


            DYt = self.pairwisedistances.run(LD)

                # Crear la matriz de coranking con las matrices de distancias
                #   Nota: Tener encuenta que , coranking(DX, DYt) es diferente a    coranking(DYt, DX)


            co = self.coranking.run(DX, DYt)



            [n, x, p, b] = self.nx_trusion.run(co)
                # n => intrusiones, x => extrusiones, b => base aleatoria, p => tasa de rangos perfectamente conservados

            Q_NX = n + x + p  # Calidad general de incrustracion, varia entre 0-1

            B_NX = x - n  # Comportamiento
            LCMC = Q_NX - b  # Meta  criterio de continuidad local
            R_NX = LCMC[0: LCMC.shape[0] - 1] / (1 - b[0: b.shape[0] - 1])  # Convertir q_nx a r_nx

            wgh = np.divide(1, np.arange(1, nbr + 1))  # 1 / np.arange(1, nbr + 1)
            wgh = np.sum(np.divide(wgh, np.sum(wgh)))  # wgh / np.sum(wgh)
            wgh = np.divide(1, np.arange(1, nbr - 1))  # 1 / np.arange(1, nbr - 1)
            wgh = np.divide(wgh, sum(wgh))  # wgh / sum(wgh)
            Ravg = np.sum(wgh * R_NX)

            return [Ravg, R_NX]

        except Exception as e:
            print(e)
            raise e
