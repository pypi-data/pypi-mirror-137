from copy import copy
from typing import List, Tuple, Dict

import numpy as np

from feature_extractor.common import DiscriminantAnalysis
from feature_extractor.indi.INDI import INDI


class MulticlassINDI(INDI):
    """
    INDI implementation for the multiclass case
    This implementation also considers faraway class searching optimization in order to improve accuracy
    """

    LDA = DiscriminantAnalysis()

    def __init__(self):
        super().__init__()
        self.ignored_classes = []
        self.classes = []

    def process(self, data: List[np.ndarray], **kwargs) -> Dict[int, Tuple[int, int]]:
        """
        Be careful, this implementation returns dictionary instead of list of layer's indices (like INDI class do)
        :return: dictionary like {'class_label': [layer_index, layer_index]}
        """
        self.ignored_classes = []
        self.classes = np.arange(len(data))
        n_classes = len(data)

        result = {}

        for _ in range(n_classes - 1):
            faraway_class_idx = self.find_faraway_class(data)
            divided_data = self.divide_data(data, faraway_class_idx)
            # Just use the method from the binary INDI implementation since now we consider One-Vs-Rest case
            indices = super().process(divided_data)
            result[faraway_class_idx] = indices

            self.ignored_classes.append(faraway_class_idx)

        result[self.get_classes_exclude_ignored()[0]] = indices
        return result

    def find_faraway_class(self, initial_data: List[np.ndarray]) -> int:
        """
        Finds faraway class in the given data using individual criteria of discriminant analysis
        :return: faraway class label
        """
        classes = self.get_classes_exclude_ignored()
        criteria_val, informative_feature_val, faraway_class = 0, 0, classes[-1]

        for _class in classes:
            data = self.divide_data(initial_data, _class)

            Sb, Sw = self.LDA.calculate_matrices(data)
            individ_criteria = self.LDA.calculate_individual_criteria(Sb, Sw)
            tmp_criteria_val = np.max(individ_criteria)

            if tmp_criteria_val > criteria_val:
                criteria_val = tmp_criteria_val
                faraway_class = _class

        return faraway_class

    def divide_data(self, data: List[np.ndarray], target: int):
        """
        Separates data in order to solve One-Vs-Rest task

        :param data: initial data
        :param target: class label which will be separated
        :return: list with two numpy arrays, the first one is "One", the second one is "Rest"
        """
        classes = self.get_classes_exclude_ignored()
        other_classes = copy(classes)
        other_classes.remove(target)
        data = [data[target], np.vstack([data[i] for i in other_classes])]
        return data

    def get_classes_exclude_ignored(self):
        return list(set(self.classes) - set(self.ignored_classes))
