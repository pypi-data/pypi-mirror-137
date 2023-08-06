from copy import copy
from typing import List

import numpy as np

from feature_extractor.common import DiscriminantAnalysis
from feature_extractor.features.Extractor import Extractor


class FeatureExtractor(Extractor):
    """
    Our primary algorithm that manage feature extraction in two steps:
        1. Find a faraway class which will be used further separately to others
            The individual criteria will be calculated and the most informative feature will be included
            into informative feature list.
        2. Find an informative features by using the group criteria until the stop condition are satisfying.

    This algorithm considers One-Vs-Rest cases (faraway class vs others)

    Stop conditions:
        1. Max number of features for a class.
        2. Difference between informativeness score before and after adding new informative feature.

    This algorithm was proposed in our paper: https://ieeexplore.ieee.org/document/9649144
    """

    LDA = DiscriminantAnalysis()

    def __init__(self):
        # This variable used to store information about the classes already calculated
        self.ignored_classes = []

        self.include_individual_feature = False
        self.stop_error = None
        self.stop_max_feat = None
        self.X = None
        self.Y = None
        self.classes = None
        self.n_classes = None

    def set_data(self, X, Y):
        self.X = X
        self.Y = Y
        self.classes = np.unique(Y)
        self.n_classes = len(self.classes)

    def find_features(self, include_individual_feature=True, stop_error=10e-3, stop_max_feat=3):
        """
        :param include_individual_feature: flags is a feature found by individual criteria considered relevant
        :param stop_error: min difference between informativeness score before and after adding new informative feature
        when algorithm stops
        :param stop_max_feat: maximum number of relevant features for each One-Vs-Rest case
        :return: list of indices of the most relevant features for the given data
        """
        self.reset_temporary_values()
        self.include_individual_feature = include_individual_feature
        self.stop_error = stop_error
        self.stop_max_feat = stop_max_feat

        features = []
        # On each iteration one class is going to be dropped (the most far away one)
        for _ in range(self.n_classes - 1):
            faraway_class = self.find_faraway_class()
            features += self.feature_extraction(faraway_class)
            self.ignored_classes.append(faraway_class)
        return np.unique(features).tolist()

    def reset_temporary_values(self):
        self.ignored_classes = []

    def feature_extraction(self, faraway_class: int) -> List[int]:
        """
        The main algorithm of feature selection. Works with One-Vs-Rest cases to search the most relevant features using
        the group criteria of the discriminant analysis.
        :param faraway_class: class label which will be separated from other in order to solve One-Vs-Rest task
        :return: list of the indices of the most relevant features
        """
        top_k_feat = []
        top_k_val = []

        data = self.divide_data(faraway_class)
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
                    temp_val = self.LDA.calculate_group_criteria(bSb, bSw)
                except Exception as e:
                    print(e)
                    continue
                if temp_val > informativeness:
                    informativeness = temp_val
                    top_feature = feature

            if informativeness - max_informativeness < self.stop_error or top_feature is None:
                break
            else:
                top_k_feat.append(top_feature)
                max_informativeness = informativeness

        return top_k_feat

    def find_faraway_class(self) -> int:
        """
        Finds faraway class in the given data using individual criteria of discriminant analysis
        :return: faraway class label
        """
        classes = self.get_classes_exclude_ignored()
        criteria_val, informative_feature_val, faraway_class = 0, 0, classes[-1]

        for _class in classes:
            data = self.divide_data(_class)

            Sb, Sw = self.LDA.calculate_matrices(data)
            individ_criteria = self.LDA.calculate_individual_criteria(Sb, Sw)
            tmp_criteria_val = np.max(individ_criteria)
            # tmp_criteria_val = self.LDA.calculate_group_criteria(Sb, Sw)

            if tmp_criteria_val > criteria_val:
                criteria_val = tmp_criteria_val
                faraway_class = _class

        return faraway_class

    def divide_data(self, target: int):
        """
        Separates data in order to solve One-Vs-Rest task
        :param target: class label which will be separated
        :return: list with two numpy arrays, the first one is "One", the second one is "Rest"
        """
        classes = self.get_classes_exclude_ignored()
        other_classes = copy(classes)
        other_classes.remove(target)
        other_classes_pos = []
        for cls in other_classes:
            other_classes_pos += np.where(np.array(self.Y, copy=False) == cls)[0].tolist()
        data = [self.X[np.where(np.array(self.Y, copy=False) == target)], self.X[other_classes_pos]]
        return data

    def get_classes_exclude_ignored(self):
        return list(set(self.classes) - set(self.ignored_classes))
