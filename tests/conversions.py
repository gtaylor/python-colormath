"""
Unit tests for color space conversions.
"""
import unittest
from colormath.colorobjs import *

class XYZConversions(unittest.TestCase):
    def setUp(self):
        color = XYZColor()
        color.xyz_x = 0.1
        color.xyz_y = 0.2
        color.xyz_z = 0.3
        self.color = color
        
    def test_conversion_to_xyy(self):
        xyy = self.color.convert_to('xyy')
        self.assertAlmostEqual(xyy.xyy_x, 0.167, 3, "XYZ to xyY failed: x coord")
        self.assertAlmostEqual(xyy.xyy_y, 0.333, 3, "XYZ to xyY failed: y coord")
        self.assertAlmostEqual(xyy.xyy_Y, 0.200, 3, "XYZ to xyY failed: Y coord")
        
    def test_conversion_to_lab(self):
        lab = self.color.convert_to('lab')
        self.assertAlmostEqual(lab.lab_l, 1.807, 3, "XYZ to Lab failed: L coord")
        self.assertAlmostEqual(lab.lab_a, -3.749, 3, "XYZ to Lab failed: a coord")
        self.assertAlmostEqual(lab.lab_b, -2.547, 3, "XYZ to Lab failed: b coord")
        
    def test_conversion_to_rgb(self):
        """
        TODO: Fix XYZ_to_RGB()
        """
        rgb = self.color.convert_to('rgb', debug=False)
        #self.assertAlmostEqual(rgb.rgb_r, 1.807, 3, "XYZ to RGB failed: R coord")
        #self.assertAlmostEqual(rgb.rgb_g, 4.532, 3, "XYZ to RGB failed: G coord")
        #self.assertAlmostEqual(rgb.rgb_b, 214.193, 3, "XYZ to RGB failed: B coord")
        
    def test_conversion_to_luv(self):
        luv = self.color.convert_to('luv')
        self.assertAlmostEqual(luv.luv_l, 1.807, 3, "XYZ to Luv failed: L coord")
        self.assertAlmostEqual(luv.luv_u, -2.564, 3, "XYZ to Luv failed: u coord")
        self.assertAlmostEqual(luv.luv_v, -0.894, 3, "XYZ to Luv failed: v coord")
        
class LabConversions(unittest.TestCase):
    def setUp(self):
        color = LabColor()
        color.lab_l = 1.807
        color.lab_a = -3.749
        color.lab_b = -2.547
        self.color = color
        
    def test_conversion_to_xyz(self):
        xyz = self.color.convert_to('xyz')
        self.assertAlmostEqual(xyz.xyz_x, 0.100, 3, "Lab to XYZ failed: X coord")
        self.assertAlmostEqual(xyz.xyz_y, 0.200, 3, "Lab to XYZ failed: Y coord")
        self.assertAlmostEqual(xyz.xyz_z, 0.300, 3, "Lab to XYZ failed: Z coord")
        
    def test_conversion_to_lchab(self):
        lch = self.color.convert_to('lchab')
        self.assertAlmostEqual(lch.lch_l, 1.807, 3, "Lab to LCH failed: L coord")
        self.assertAlmostEqual(lch.lch_c, 4.532, 3, "Lab to LCH failed: C coord")
        self.assertAlmostEqual(lch.lch_h, 214.191, 3, "Lab to LCH failed: H coord")
        
class LCHabConversions(unittest.TestCase):
    def setUp(self):
        color = LCHabColor()
        color.lch_l = 1.807
        color.lch_c = 4.532
        color.lch_h = 214.191
        self.color = color
                
    def test_conversion_to_lab(self):
        lab = self.color.convert_to('lab')
        self.assertAlmostEqual(lab.lab_l, 1.807, 3, "LCHab to Lab failed: L coord")
        self.assertAlmostEqual(lab.lab_a, -3.749, 3, "LCHab to Lab failed: a coord")
        self.assertAlmostEqual(lab.lab_b, -2.547, 3, "LCHab to Lab failed: b coord")
        
class LCHuvConversions(unittest.TestCase):
    def setUp(self):
        color = LCHuvColor()
        color.lch_l = 1.807
        color.lch_c = 2.715
        color.lch_h = 199.228
        self.color = color
                
    def test_conversion_to_luv(self):
        luv = self.color.convert_to('luv')
        self.assertAlmostEqual(luv.luv_l, 1.807, 3, "LCHuv to Luv failed: L coord")
        self.assertAlmostEqual(luv.luv_u, -2.564, 3, "LCHuv to Luv failed: u coord")
        self.assertAlmostEqual(luv.luv_v, -0.894, 3, "LCHuv to Luv failed: v coord")

if __name__ == '__main__':
    unittest.main()