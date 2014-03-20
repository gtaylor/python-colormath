"""
Tests for color difference (Delta E) equations.
"""

import unittest

from colormath.color_objects import XYZColor


# noinspection PyPep8Naming
class chromaticAdaptationTestCase(unittest.TestCase):
    def setUp(self):
        self.color = XYZColor(0.5, 0.4, 0.1, illuminant='C')
        
    def test_adaptation_c_to_d65(self):
        self.color.apply_adaptation(target_illuminant='D65')
        self.assertAlmostEqual(
            self.color.xyz_x, 0.491, 3,
            "C to D65 adaptation failed: X coord")
        self.assertAlmostEqual(
            self.color.xyz_y, 0.400, 3,
            "C to D65 adaptation failed: Y coord")
        self.assertAlmostEqual(
            self.color.xyz_z, 0.093, 3,
            "C to D65 adaptation failed: Z coord")
        self.assertEqual(
            self.color.illuminant, 'd65',
            "C to D65 adaptation failed: Illuminant transfer")
