from copy import copy
from typing import List

import numpy as np

from feature_extractor.common import DiscriminantAnalysis
from feature_extractor.features.Extractor import Extractor


class ICDA(Extractor):
    """
    Feature selection using "Individual Criteria Disriminant Analysis" considering One-Vs-Rest cases
    """

    LDA = DiscriminantAnalysis()

    def __init__(self):
        self.X = None
        self.Y = None
        self.classes = None
        self.n_classes = None
        self.max_features_per_class = None

    def set_data(self, X, Y):
        self.X = X
        self.Y = Y
        self.classes = np.unique(Y)
        self.n_classes = len(self.classes)
        self.max_features_per_class = None

    def find_features(self, max_features_per_class=3):
        """
        :param max_features_per_class: maximum number of relevant features for each One-Vs-Rest case
        :return: list of indices of the most relevant features for the given data
        """
        self.max_features_per_class = max_features_per_class

        features = []
        for class_id in self.classes:
            features += self.feature_extraction(class_id)
        return np.unique(features).tolist()

    def feature_extraction(self, class_id: int) -> List[int]:
        top_k_feat = []

        data = self.divide_data(class_id)
        Sb, Sw = self.LDA.calculate_matrices(data)

        individual_criteria = self.LDA.calculate_individual_criteria(Sb, Sw).tolist()
        for i in range(self.max_features_per_class):
            top_k_feat.append(np.argmax(individual_criteria))
            individual_criteria.remove(individual_criteria[top_k_feat[-1]])
        return top_k_feat

    def divide_data(self, target: int):
        """
        Separates data in order to solve One-Vs-Rest task
        :param target: class labels which will be separated
        :return: list with two numpy arrays, the first one is "One", the second one is "Rest"
        """
        other_classes = list(copy(self.classes))
        other_classes.remove(target)
        other_classes_pos = []
        for cls in other_classes:
            other_classes_pos += np.where(np.array(self.Y, copy=False) == cls)[0].tolist()
        data = [self.X[np.where(np.array(self.Y, copy=False) == target)], self.X[other_classes_pos]]
        return data
