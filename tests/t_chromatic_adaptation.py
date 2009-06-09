"""
 Color Math Module (colormath) 
 Copyright (C) 2009 Gregory Taylor

 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

"""
Tests for color difference (Delta E) equations.
"""
import unittest
from colormath.color_objects import *
from colormath.color_exceptions import *

class Chromatic_Adaptation(unittest.TestCase):
    def setUp(self):
        self.color = XYZColor(0.5, 0.4, 0.1, illuminant='C')
        
    def test_adaptation_c_to_d65(self):
        self.color.apply_adaptation(target_illuminant='D65')
        self.assertAlmostEqual(self.color.xyz_x, 0.491, 3, 
                               "C to D65 adaptation failed: X coord")
        self.assertAlmostEqual(self.color.xyz_y, 0.400, 3, 
                               "C to D65 adaptation failed: Y coord")
        self.assertAlmostEqual(self.color.xyz_z, 0.093, 3, 
                               "C to D65 adaptation failed: Z coord")
        self.assertEqual(self.color.illuminant, 'd65', 
                               "C to D65 adaptation failed: Illuminant transfer")
        
if __name__ == '__main__':
    unittest.main()