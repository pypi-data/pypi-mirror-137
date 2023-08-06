import itertools
from typing import List

import numpy as np

from feature_extractor.common import DiscriminantAnalysis
from feature_extractor.features.Extractor import Extractor


class FeatureExtractor(Extractor):
    """
    Second version of the algorithm which based on feature selection for each pair of classes i.e. considers One-Vs-One
    cases.

    May be slower than other versions. Tends to produce result worse than other versions.
    """

    LDA = DiscriminantAnalysis()

    def __init__(self):
        self.include_individual_feature = False
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
        self.include_individual_feature = include_individual_feature

        features = []
        # Iterate over all pairs of classes except pairs like (x, x)
        for class_1, class_2 in itertools.permutations(self.classes, 2):
            features += self.feature_extraction(class_1, class_2)
        return np.unique(features).tolist()

    def feature_extraction(self, class_1: int, class_2: int) -> List[int]:
        """
        The secondary algorithm of feature selection. Works with One-Vs-One cases to search the most relevant features
        using the group criteria of the discriminant analysis.
        :return: list of the indices of the most relevant features
        """
        top_k_feat = []
        top_k_val = []

        data = self.divide_data(class_1, class_2)
        Sb, Sw = self.LDA.calculate_matrices(data)
        n_features = Sb.shape[0]

        if self.include_individual_feature:
            individual_criteria = self.LDA.calculate_individual_criteria(Sb, Sw)
            top_k_feat.append(np.argmax(individual_criteria))
            top_k_val.append(np.max(individual_criteria))

        informativeness = 0.0

        for i in range(1):
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
                    top_feature = feature

            top_k_feat.append(top_feature)

        return top_k_feat

    def divide_data(self, class_1, class_2):
        data = [self.X[self.Y == class_1], self.X[self.Y == class_2]]
        return data
