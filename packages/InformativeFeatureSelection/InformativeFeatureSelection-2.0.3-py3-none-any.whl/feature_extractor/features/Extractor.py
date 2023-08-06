from abc import abstractmethod, ABC
from typing import List

import numpy as np


class Extractor(ABC):

    @abstractmethod
    def set_data(self, X: np.ndarray, Y: np.ndarray):
        """
        :param X: numpy array of shape (n_samples, n_features)
        :param Y: numpy array of shape (n_samples, n_features)
        """
        pass

    @abstractmethod
    def find_features(self, **kwargs) -> List[int]:
        """
        Feature extraction algorithm entry point
        :param kwargs: takes arguments specific for the feature extractor
        :return: list of indices of the most relevant features for the given data
        """
        pass
