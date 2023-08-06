import unittest

import numpy as np
from sklearn.datasets import load_iris, load_wine
from feature_extractor.features.FeatureExtractorWithFarawayClasses import FeatureExtractor as Fe1
from feature_extractor.features.FeatureExtractorPairsCheck import FeatureExtractor as Fe2
from feature_extractor.features.FeatureExtractorNaive import FeatureExtractor as Fe3

from feature_extractor.features.ICDA import ICDA


class FirstFeatureExtractorHardTestCase(unittest.TestCase):
    def test_algorithm(self):
        X, Y = np.load('X_train.npy'), np.load('y_train.npy')
        fe = Fe1()
        fe.set_data(X, Y)
        result = fe.find_features()
        self.assertIsNotNone(result)
        print(f'Fe1 = {result}')


class FirstFeatureExtractorTestCase(unittest.TestCase):
    def test_whole_algorithm(self):
        X, Y = load_iris(return_X_y=True)
        fe = Fe1()
        fe.set_data(X, Y)
        result = fe.find_features(include_individual_feature=False)
        self.assertIsNotNone(result)
        print(f'Fe1:(Iris dataset) = {result}')

    def test_whole_algorithm_hard_dataset(self):
        X, Y = load_wine(return_X_y=True)
        fe = Fe1()
        fe.set_data(X, Y)
        result = fe.find_features(stop_max_feat=1)
        self.assertIsNotNone(result)
        print(f'Fe1:(Wine dataset) = {result}')


class SecondFeatureExtractorTestCase(unittest.TestCase):
    def test_whole_algorithm(self):
        X, Y = load_iris(return_X_y=True)
        fe = Fe2()
        fe.set_data(X, Y)
        result = fe.find_features(include_individual_feature=True)
        self.assertIsNotNone(result)
        print(f'Fe2:(Iris dataset) = {result}')

    def test_whole_algorithm_hard_dataset(self):
        X, Y = load_wine(return_X_y=True)
        fe = Fe2()
        fe.set_data(X, Y)
        result = fe.find_features(include_individual_feature=True)
        self.assertIsNotNone(result)
        print(f'Fe2:(Wine dataset) = {result}')


class ThirdFeatureExtractorTestCase(unittest.TestCase):
    def test_whole_algorithm(self):
        X, Y = load_iris(return_X_y=True)
        fe = Fe3()
        fe.set_data(X, Y)
        result = fe.find_features(include_individual_feature=True, stop_max_feat=1)
        self.assertIsNotNone(result)
        print(f'Fe3:(Iris dataset) = {result}')

    def test_whole_algorithm_hard_dataset(self):
        X, Y = load_wine(return_X_y=True)
        fe = Fe3()
        fe.set_data(X, Y)
        result = fe.find_features(include_individual_feature=True, stop_max_feat=1)
        self.assertIsNotNone(result)
        print(f'Fe3:(Wine dataset) = {result}')


class IcdaExtractorTestCase(unittest.TestCase):
    def test_whole_algorithm(self):
        X, Y = load_iris(return_X_y=True)
        fe = ICDA()
        fe.set_data(X, Y)
        result = fe.find_features()
        self.assertIsNotNone(result)
        print(f'ICDA:(Iris dataset) = {result}')

    def test_whole_algorithm_hard_dataset(self):
        X, Y = load_wine(return_X_y=True)
        fe = ICDA()
        fe.set_data(X, Y)
        result = fe.find_features()
        self.assertIsNotNone(result)
        print(f'ICDA:(Wine dataset) = {result}')


if __name__ == '__main__':
    unittest.main()
