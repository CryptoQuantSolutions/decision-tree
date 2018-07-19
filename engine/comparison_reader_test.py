import unittest
import engine.comparison_reader as comparison_reader

class ComparisonMgrTest(unittest.TestCase):
    def setUp(self):
        self.comp_test_class = comparison_reader.ComparisonsMgr()

    def test_binarySearchAlgorithm(self):
        self.eval_comps()