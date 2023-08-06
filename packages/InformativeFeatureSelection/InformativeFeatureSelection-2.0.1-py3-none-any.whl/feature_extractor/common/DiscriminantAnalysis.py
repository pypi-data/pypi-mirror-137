from typing import Tuple, Union, List, Any

import numpy as np
from numba import njit


@njit
def single_feature_statistic(data: Union[np.ndarray, List[np.ndarray]]) -> Tuple[np.ndarray, np.ndarray, Any]:
    """
    Method optimized for calculation individual criteria for single feature.
    Work twice faster that "numba_calculate_matrices"
    :return: scatter_between value, scatter_within value and individual criteria value
    """
    n_classes = len(data)
    separated_into_classes = data
    aig = np.array([np.mean(obj) for obj in separated_into_classes])

    n_k = np.array([class_samples.shape[0] for class_samples in separated_into_classes])
    n = np.sum(n_k)

    wa = np.sum(aig * n_k / n)

    b = np.sum(n_k * (aig - wa) ** 2)
    w = np.sum(np.array([np.sum((separated_into_classes[i] - aig[i]) ** 2) for i in range(0, n_classes)]))

    _lambda = b / (w + b)
    return b, w, _lambda


@njit
def numba_calculate_matrices(data: Union[np.ndarray, List[np.ndarray]]) -> Tuple[np.ndarray, np.ndarray]:
    n_features = data[0].shape[1]
    Sb = np.zeros((n_features, n_features))
    Sw = np.zeros((n_features, n_features))
    mean_vectors = np.zeros((len(data), n_features,))
    mean = np.zeros((n_features, 1))

    for class_idx, class_samples in enumerate(data):
        for feature_idx in range(n_features):
            mean_vectors[class_idx, feature_idx] = np.mean(class_samples[::, feature_idx])
    for feature_idx in range(n_features):
        mean[feature_idx] = np.mean(mean_vectors[::, feature_idx])

    for cl in range(len(data)):
        if data[cl].shape[1] == 1:
            # np.cov does not work with data of shape (N, 1) =)
            Sw += data[cl].shape[0] * np.cov(data[cl][::, 0].T)
        else:
            Sw += data[cl].shape[0] * np.cov(data[cl].T)

    for cl, mean_v in enumerate(mean_vectors):
        n = data[cl].shape[0]
        Sb += n * (mean_v - mean).dot(np.transpose(mean_v - mean))

    return Sb, Sw


@njit
def numba_calculate_individual_criteria(Sb, Sw):
    return np.diag(Sb) / np.diag(Sw + Sb)


@njit
def numba_calculate_group_criteria(Sb, Sw):
    try:
        return np.trace(np.linalg.inv(Sw + Sb).dot(Sb))
    except:
        return np.trace(np.linalg.pinv(Sw + Sb).dot(Sb))


class DiscriminantAnalysis:

    def calculate_individual_criteria(self, Sb: np.ndarray, Sw: np.ndarray) -> np.array:
        return numba_calculate_individual_criteria(Sb, Sw)

    def calculate_group_criteria(self, Sb: np.ndarray, Sw: np.ndarray) -> float:
        return numba_calculate_group_criteria(Sb, Sw)

    def calculate_matrices(self, data: Union[np.ndarray, List[np.ndarray]]) \
            -> Union[Tuple[np.ndarray, np.ndarray], Tuple[np.ndarray, np.ndarray, Any]]:
        """
        Calculates scatter between and scatter within matrices
        :see Linear discriminant analysis

        :note if data with single feature is provided also returns individual criteria value. It also may be usefully
        with extremely large data

        :param data: numpy array of shape (n_classes, n_samples, n_features) or list of numpy arrays (n_classes, ?,
        n_features)
        :return: tuple of two numpy arrays which represents scatter between and scatter within matrices
        """
        if data[0].shape[1] == 1:
            return single_feature_statistic(data)
        return numba_calculate_matrices(data)
