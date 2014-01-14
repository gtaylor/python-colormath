"""
Tests for color difference (Delta E) equations.
"""
import unittest
from colormath.color_objects import *
from colormath.color_exceptions import *
from colormath import color_diff_matrix

import numpy as np

class DeltaE_Tests(unittest.TestCase):
    def setUp(self):
        self.color_lab = LabColor(lab_l=0.9, lab_a=16.3, lab_b=-2.22)

        self.color_lab_matrix = np.array([
            [0.7, 14.2, -1.80],
            [69.34, -0.88, -52.57],
        ])

    def test_cie1976_accuracy(self):
        results = color_diff_matrix.delta_e(self.color_lab, self.color_lab_matrix, mode='cie1976')

        expected = np.array([2.151, 86.685])

        self.assertAlmostEqual(results[0], expected[0], 3,
            "DeltaE CIE1976 formula error. Got %s, expected %s." % (results[0], expected[0]))

        self.assertAlmostEqual(results[1], expected[1], 3,
            "DeltaE CIE1976 formula error. Got %s, expected %s." % (results[1], expected[1]))

    def test_cie1994_accuracy(self):
        results = color_diff_matrix.delta_e(self.color_lab, self.color_lab_matrix, mode='cie1994')

        expected = np.array([1.249, 78.0778])

        self.assertAlmostEqual(results[0], expected[0], 3,
            "DeltaE CIE1994 formula error. Got %s, expected %s." % (results[0], expected[0]))

        self.assertAlmostEqual(results[1], expected[1], 3,
            "DeltaE CIE1994 formula error. Got %s, expected %s." % (results[1], expected[1]))

    def test_cie1994_accuracy_textile(self):
        results = color_diff_matrix.delta_e(self.color_lab, self.color_lab_matrix, mode='cie1994',
                                            K_1=0.048, K_2=0.014, K_L=2)

        expected = np.array([1.204, 50.854])

        self.assertAlmostEqual(results[0], expected[0], 3,
            "DeltaE CIE1994 (textiles) formula error. Got %.3f, expected %.3f." % (results[0], expected[0]))

        self.assertAlmostEqual(results[1], expected[1], 3,
            "DeltaE CIE1994 (textiles) formula error. Got %.3f, expected %.3f." % (results[1], expected[1]))

