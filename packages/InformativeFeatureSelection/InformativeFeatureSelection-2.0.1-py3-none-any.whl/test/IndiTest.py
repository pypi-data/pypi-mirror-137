import unittest
from timeit import timeit

import numpy as np
import json

from feature_extractor.indi.INDI import INDI
from feature_extractor.indi.IndiBase import BaseINDI
from feature_extractor.indi.Multiclass_INDI import MulticlassINDI


class IndiTest(unittest.TestCase):
    def test_default_indi(self):
        specter = np.load('True sailnas.npy').transpose((1, 2, 0))  # (C, H, W) -> (H, W, C)
        with open("mask_points.json", 'r') as f:
            points = list(json.load(f).values())
        labels = [1, 2]
        indi_solver: BaseINDI = INDI()
        best = indi_solver.process_from_points(specter, points, labels)
        print(f'Solution = {best} ')

        t = timeit(lambda: indi_solver.process_from_points(specter, points, labels), number=10) / 10
        print(t)
        self.assertIsNotNone(t)

    def test_multiclass_indi(self):
        specter = np.load('True sailnas.npy').transpose((1, 2, 0))  # (C, H, W) -> (H, W, C)
        with open("mask_points.json", 'r') as f:
            points = list(json.load(f).values())
        labels = [1, 2]
        indi_solver: BaseINDI = MulticlassINDI()
        best = indi_solver.process_from_points(specter, points, labels)
        print(f'Solution = {best}')

        t = timeit(lambda: indi_solver.process_from_points(specter, points, labels), number=10) / 10
        print(t)
        self.assertIsNotNone(t)


if __name__ == '__main__':
    unittest.main()
