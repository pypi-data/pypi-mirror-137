from copy import copy
from typing import List

import numpy as np

from feature_extractor.common import DiscriminantAnalysis
from feature_extractor.features.Extractor import Extractor


class FeatureExtractor(Extractor):
    """
    Searches for the most informative features regardless faraway class selection.
    Solves feature selection task by searching features for each One-Vs-Rest case (except one)
    """

    LDA = DiscriminantAnalysis()

    def __init__(self):
        self.include_individual_feature = False
        self.X = None
        self.Y = None
        self.classes = None
        self.n_classes = None
        self.stop_error = None
        self.stop_max_feat = None

    def set_data(self, X, Y):
        self.X = X
        self.Y = Y
        self.classes = np.unique(Y)
        self.n_classes = len(self.classes)

    def find_features(self, include_individual_feature=True, stop_error=10e-3, stop_max_feat=3) -> List[int]:
        """
        :param include_individual_feature: flags is a feature found by individual criteria considered relevant
        :param stop_error: min difference between informativeness score before and after adding new informative feature
        when algorithm stops
        :param stop_max_feat: maximum number of relevant features for each One-Vs-Rest case
        :return: list of indices of the most relevant features for the given data
        """
        self.include_individual_feature = include_individual_feature
        self.stop_error = stop_error
        self.stop_max_feat = stop_max_feat

        features = []
        for class_id in self.classes[:-1]:
            features += self.feature_extraction(class_id)
        return np.unique(features).tolist()

    def feature_extraction(self, class_id: int) -> List[int]:
        """
        The main algorithm of feature selection. Works with One-Vs-Rest cases to search the most relevant features using
        the group criteria of the discriminant analysis.
        :param class_id: class label which will be separated from other in order to solve One-Vs-Rest task
        :return: list of the indices of the most relevant features
        """
        top_k_feat = []
        top_k_val = []

        data = self.divide_data(class_id)
        Sb, Sw = self.LDA.calculate_matrices(data)
        n_features = Sb.shape[0]

        if self.include_individual_feature:
            individual_criteria = self.LDA.calculate_individual_criteria(Sb, Sw)
            top_k_feat.append(np.argmax(individual_criteria))
            top_k_val.append(np.max(individual_criteria))

        informativeness = 0.0
        max_informativeness = 0.0

        for i in range(self.stop_max_feat):
            top_feature = None
            for feature in range(n_features):
                if i in top_k_feat:
                    continue

                selection = (*top_k_feat, feature)
                bSw = Sw[selection,][:, selection]
                bSb = Sb[selection,][:, selection]

                try:
                    temp_informativeness = self.LDA.calculate_group_criteria(bSb, bSw)
                except Exception as e:
                    print(e)
                    continue
                if temp_informativeness > informativeness:
                    informativeness = temp_informativeness
                    top_feature = feature

            if informativeness - max_informativeness < self.stop_error or top_feature is None:
                break
            else:
                top_k_feat.append(top_feature)
                max_informativeness = informativeness

        return top_k_feat

    def divide_data(self, target: int) -> List[np.ndarray]:
        """
        Separates data in order to solve One-Vs-Rest task
        :param target: class label which will be separated
        :return: list with two numpy arrays, the first one is "One", the second one is "Rest"
        """
        other_classes = list(copy(self.classes))
        other_classes.remove(target)
        other_classes_pos = []
        for cls in other_classes:
            other_classes_pos += np.where(np.array(self.Y, copy=False) == cls)[0].tolist()
        data = [self.X[np.where(np.array(self.Y, copy=False) == target)], self.X[other_classes_pos]]
        return data
