"""
Tests for color difference (Delta E) equations.
"""

import unittest

import numpy as np

from colormath.color_objects import LabColor


class DeltaEMatrixTestCase(unittest.TestCase):
    def setUp(self):
        self.color_lab = LabColor(lab_l=0.9, lab_a=16.3, lab_b=-2.22)

        self.color_lab_matrix = np.array([
            [0.7, 14.2, -1.80],
            [69.34, -0.88, -52.57],
        ])

    def test_cie1976_accuracy(self):
        results = self.color_lab.delta_e_matrix(self.color_lab_matrix, mode='cie1976')

        expected = np.array([2.151, 86.685])

        self.assertAlmostEqual(results[0], expected[0], 3,
            "DeltaE CIE1976 formula error. Got %s, expected %s." % (
                results[0], expected[0]))

        self.assertAlmostEqual(results[1], expected[1], 3,
            "DeltaE CIE1976 formula error. Got %s, expected %s." % (
                results[1], expected[1]))

    def test_cie1994_accuracy(self):
        results = self.color_lab.delta_e_matrix(self.color_lab_matrix, mode='cie1994')

        expected = np.array([1.249, 78.0778])

        self.assertAlmostEqual(results[0], expected[0], 3,
            "DeltaE CIE1994 formula error. Got %s, expected %s." % (
                results[0], expected[0]))

        self.assertAlmostEqual(results[1], expected[1], 3,
            "DeltaE CIE1994 formula error. Got %s, expected %s." % (
                results[1], expected[1]))

    def test_cie1994_accuracy_textile(self):
        results = self.color_lab.delta_e_matrix(self.color_lab_matrix, mode='cie1994',
                                                K_1=0.048, K_2=0.014, K_L=2)

        expected = np.array([1.204, 50.854])

        self.assertAlmostEqual(results[0], expected[0], 3,
            "DeltaE CIE1994 (textiles) formula error. Got %.3f, expected %.3f." % (
                results[0], expected[0]))

        self.assertAlmostEqual(results[1], expected[1], 3,
            "DeltaE CIE1994 (textiles) formula error. Got %.3f, expected %.3f." % (
                results[1], expected[1]))

    def test_cmc_accuracy(self):
        # 2:1
        results = self.color_lab.delta_e_matrix(self.color_lab_matrix, mode='cmc', pl=2, pc=1)

        expected = np.array([1.443, 79.820])

        self.assertAlmostEqual(results[0], expected[0], 3,
            "DeltaE CMC formula error. Got %s, expected %s." % (
                results[0], expected[0]))

        self.assertAlmostEqual(results[1], expected[1], 3,
            "DeltaE CMC formula error. Got %s, expected %s." % (
                results[1], expected[1]))

        # 1:1
        results = self.color_lab.delta_e_matrix(self.color_lab_matrix, mode='cmc', pl=1, pc=1)

        expected = np.array([1.482, 140.801])

        self.assertAlmostEqual(results[0], expected[0], 3,
            "DeltaE CMC formula error. Got %s, expected %s." % (
                results[0], expected[0]))

        self.assertAlmostEqual(results[1], expected[1], 3,
            "DeltaE CMC formula error. Got %s, expected %s." % (
                results[1], expected[1]))

    def test_cie2000_accuracy(self):
        results = self.color_lab.delta_e_matrix(self.color_lab_matrix, mode='cie2000')

        expected = np.array([1.523, 65.653])

        self.assertAlmostEqual(results[0], expected[0], 3,
            "DeltaE CIE2000 formula error. Got %s, expected %s." % (
                results[0], expected[0]))

        self.assertAlmostEqual(results[1], expected[1], 3,
            "DeltaE CIE2000 formula error. Got %s, expected %s." % (
                results[1], expected[1]))

    def test_cie2000_accuracy_2(self):

        color1 = (
            LabColor(lab_l=50.0000, lab_a=2.6772, lab_b=-79.7751),
            LabColor(lab_l=50.0000, lab_a=3.1571, lab_b=-77.2803),
            LabColor(lab_l=50.0000, lab_a=2.8361, lab_b=-74.0200),
            LabColor(lab_l=50.0000, lab_a=-1.3802, lab_b=-84.2814),
            LabColor(lab_l=50.0000, lab_a=-1.1848, lab_b=-84.8006),
            LabColor(lab_l=50.0000, lab_a=-0.9009, lab_b=-85.5211),
            LabColor(lab_l=50.0000, lab_a=0.0000, lab_b=0.0000),
            LabColor(lab_l=50.0000, lab_a=-1.0000, lab_b=2.0000),
            LabColor(lab_l=50.0000, lab_a=2.4900, lab_b=-0.0010),
            LabColor(lab_l=50.0000, lab_a=2.4900, lab_b=-0.0010),
            LabColor(lab_l=50.0000, lab_a=2.4900, lab_b=-0.0010),
            LabColor(lab_l=50.0000, lab_a=2.4900, lab_b=-0.0010),
            LabColor(lab_l=50.0000, lab_a=-0.0010, lab_b=2.4900),
            LabColor(lab_l=50.0000, lab_a=-0.0010, lab_b=2.4900),
            LabColor(lab_l=50.0000, lab_a=-0.0010, lab_b=2.4900),
            LabColor(lab_l=50.0000, lab_a=2.5000, lab_b=0.0000),
            LabColor(lab_l=50.0000, lab_a=2.5000, lab_b=0.0000),
            LabColor(lab_l=50.0000, lab_a=2.5000, lab_b=0.0000),
            LabColor(lab_l=50.0000, lab_a=2.5000, lab_b=0.0000),
            LabColor(lab_l=50.0000, lab_a=2.5000, lab_b=0.0000),
            LabColor(lab_l=50.0000, lab_a=2.5000, lab_b=0.0000),
            LabColor(lab_l=50.0000, lab_a=2.5000, lab_b=0.0000),
            LabColor(lab_l=50.0000, lab_a=2.5000, lab_b=0.0000),
            LabColor(lab_l=50.0000, lab_a=2.5000, lab_b=0.0000),
            LabColor(lab_l=60.2574, lab_a=-34.0099, lab_b=36.2677),
            LabColor(lab_l=63.0109, lab_a=-31.0961, lab_b=-5.8663),
            LabColor(lab_l=61.2901, lab_a=3.7196, lab_b=-5.3901),
            LabColor(lab_l=35.0831, lab_a=-44.1164, lab_b=3.7933),
            LabColor(lab_l=22.7233, lab_a=20.0904, lab_b=-46.6940),
            LabColor(lab_l=36.4612, lab_a=47.8580, lab_b=18.3852),
            LabColor(lab_l=90.8027, lab_a=-2.0831, lab_b=1.4410),
            LabColor(lab_l=90.9257, lab_a=-0.5406, lab_b=-0.9208),
            LabColor(lab_l=6.7747, lab_a=-0.2908, lab_b=-2.4247),
            LabColor(lab_l=2.0776, lab_a=0.0795, lab_b=-1.1350),
        )

        color2 = np.array([
            [50.0000, 0.0000, -82.7485],
            [50.0000, 0.0000, -82.7485],
            [50.0000, 0.0000, -82.7485],
            [50.0000, 0.0000, -82.7485],
            [50.0000, 0.0000, -82.7485],
            [50.0000, 0.0000, -82.7485],
            [50.0000, -1.0000, 2.0000],
            [50.0000, 0.0000, 0.0000],
            [50.0000, -2.4900, 0.0009],
            [50.0000, -2.4900, 0.0010],
            [50.0000, -2.4900, 0.0011],
            [50.0000, -2.4900, 0.0012],
            [50.0000, 0.0009, -2.4900],
            [50.0000, 0.0010, -2.4900],
            [50.0000, 0.0011, -2.4900],
            [50.0000, 0.0000, -2.5000],
            [73.0000, 25.0000, -18.0000],
            [61.0000, -5.0000, 29.0000],
            [56.0000, -27.0000, -3.0000],
            [58.0000, 24.0000, 15.0000],
            [50.0000, 3.1736, 0.5854],
            [50.0000, 3.2972, 0.0000],
            [50.0000, 1.8634, 0.5757],
            [50.0000, 3.2592, 0.3350],
            [60.4626, -34.1751, 39.4387],
            [62.8187, -29.7946, -4.0864],
            [61.4292, 2.2480, -4.9620],
            [35.0232, -40.0716, 1.5901],
            [23.0331, 14.9730, -42.5619],
            [36.2715, 50.5065, 21.2231],
            [91.1528, -1.6435, 0.0447],
            [88.6381, -0.8985, -0.7239],
            [5.8714, -0.0985, -2.2286],
            [0.9033, -0.0636, -0.5514],
        ])

        diff = [
            2.0425, 2.8615, 3.4412, 1.0000, 1.0000,
            1.0000, 2.3669, 2.3669, 7.1792, 7.1792,
            7.2195, 7.2195, 4.8045, 4.8045, 4.7461,
            4.3065, 27.1492, 22.8977, 31.9030, 19.4535,
            1.0000, 1.0000, 1.0000, 1.0000, 1.2644,
            1.2630, 1.8731, 1.8645, 2.0373, 1.4146,
            1.4441, 1.5381, 0.6377, 0.9082
        ]

        for i, color in enumerate(color1):
            deltas = color.delta_e_matrix(color2, mode='cie2000')
            result = deltas[i]
            expected = diff[i]

            self.assertAlmostEqual(result, expected, 4,
                "DeltaE CIE2000 formula error. Got %.4f, expected %.4f" % (
                    result, expected))

