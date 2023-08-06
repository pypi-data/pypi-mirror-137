import unittest

import numpy as np

from feature_extractor.common import DiscriminantAnalysis


class DiscriminantAnalysisTestCase(unittest.TestCase):
    def test_its_working_without_errors(self):
        data = [np.random.randn(100, 10) for i in range(2)]

        lda = DiscriminantAnalysis()
        Sb, Sw = lda.calculate_matrices(data)
        i_cr = lda.calculate_individual_criteria(Sb, Sw)
        g_cr = lda.calculate_group_criteria(Sb, Sw)
        self.assertIsNotNone(g_cr)


if __name__ == '__main__':
    unittest.main()
