from typing import List, Tuple

import numpy as np

from feature_extractor.common import DiscriminantAnalysis
from feature_extractor.indi.IndiBase import BaseINDI


def ndi(l1: np.ndarray, l2: np.ndarray) -> np.ndarray:
    return np.divide(l1 - l2, l1 + l2, out=np.zeros_like(l1), where=l2 != 0, dtype=np.float32)


class INDI(BaseINDI):
    """
    INDI implementation for the binary case
    """

    lda = DiscriminantAnalysis()

    def process(self, data: List[np.ndarray], **kwargs) -> Tuple[int, int]:
        n_classes = len(data)
        assert n_classes == 2, "This is implementation of binary INDI"
        n_features = data[0].shape[1]
        max_lambda = np.NINF
        best_layers = (1, 2)

        data = [class_samples / class_samples.max(axis=0) for class_samples in data]

        for i in range(n_features):
            for j in range(i + 1):
                if i != j:
                    ndi_cl1 = ndi(data[0][::, i], data[0][::, j])
                    ndi_cl2 = ndi(data[1][::, i], data[1][::, j])

                    _, _, _lambda = self.lda.calculate_matrices([ndi_cl1.reshape(-1, 1), ndi_cl2.reshape(-1, 1)])

                    if _lambda > max_lambda:
                        best_layers = (i, j)
                        max_lambda = _lambda
        return best_layers
