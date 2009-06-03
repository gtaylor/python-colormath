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
Various tests for color objects.
"""
import unittest
from colormath.color_objects import *
from colormath.color_exceptions import *

class SpectralConversions(unittest.TestCase):
    def setUp(self):
        """
        While it is possible to specify the entire spectral color using
        positional arguments, set this thing up with keywords for the ease of
        manipulation.
        """
        color = SpectralColor(spec_380nm=0.0600, spec_390nm=0.0600, spec_400nm=0.0641,
                        spec_410nm=0.0654, spec_420nm=0.0645, spec_430nm=0.0605,
                        spec_440nm=0.0562, spec_450nm=0.0543, spec_460nm=0.0537,
                        spec_470nm=0.0541, spec_480nm=0.0559, spec_490nm=0.0603,
                        spec_500nm=0.0651, spec_510nm=0.0680, spec_520nm=0.0705,
                        spec_530nm=0.0736, spec_540nm=0.0772, spec_550nm=0.0809,
                        spec_560nm=0.0870, spec_570nm=0.0990, spec_580nm=0.1128,
                        spec_590nm=0.1251, spec_600nm=0.1360, spec_610nm=0.1439,
                        spec_620nm=0.1511, spec_630nm=0.1590, spec_640nm=0.1688,
                        spec_650nm=0.1828, spec_660nm=0.1996, spec_670nm=0.2187,
                        spec_680nm=0.2397, spec_690nm=0.2618, spec_700nm=0.2852,
                        spec_710nm=0.2500, spec_720nm=0.2400, spec_730nm=0.2300)
        self.color = color
                
    def test_conversion_to_xyz(self):
        xyz = self.color.convert_to('xyz')
        self.assertAlmostEqual(xyz.xyz_x, 0.115, 3, "Spectral to XYZ failed: X coord")
        self.assertAlmostEqual(xyz.xyz_y, 0.099, 3, "Spectral to XYZ failed: Y coord")
        self.assertAlmostEqual(xyz.xyz_z, 0.047, 3, "Spectral to XYZ failed: Z coord")
        
    def test_convert_to_self(self):
        same_color = self.color.convert_to('spectral')
        self.assertEqual(self.color, same_color)

class XYZConversions(unittest.TestCase):
    def setUp(self):
        self.color = XYZColor(0.1, 0.2, 0.3)
        
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
        rgb = self.color.convert_to('rgb')
        self.assertEqual(rgb.rgb_r, 0, "XYZ to RGB failed: R coord")
        self.assertEqual(rgb.rgb_g, 10, "XYZ to RGB failed: G coord")
        self.assertEqual(rgb.rgb_b, 12, "XYZ to RGB failed: B coord")
        
    def test_conversion_to_luv(self):
        luv = self.color.convert_to('luv')
        self.assertAlmostEqual(luv.luv_l, 1.807, 3, "XYZ to Luv failed: L coord")
        self.assertAlmostEqual(luv.luv_u, -2.564, 3, "XYZ to Luv failed: u coord")
        self.assertAlmostEqual(luv.luv_v, -0.894, 3, "XYZ to Luv failed: v coord")
        
    def test_convert_to_self(self):
        same_color = self.color.convert_to('xyz')
        self.assertEqual(self.color, same_color)
        
class xyYConversions(unittest.TestCase):
    def setUp(self):
        self.color = xyYColor(0.167, 0.333, 0.200)
        
    def test_conversion_to_xyz(self):
        xyz = self.color.convert_to('xyz')
        self.assertAlmostEqual(xyz.xyz_x, 0.100, 3, "xyY to XYZ failed: X coord")
        self.assertAlmostEqual(xyz.xyz_y, 0.200, 3, "xyY to XYZ failed: Y coord")
        self.assertAlmostEqual(xyz.xyz_z, 0.300, 3, "xyY to XYZ failed: Z coord")
        
    def test_convert_to_self(self):
        same_color = self.color.convert_to('xyy')
        self.assertEqual(self.color, same_color)
        
class LabConversions(unittest.TestCase):
    def setUp(self):
        self.color = LabColor(1.807, -3.749, -2.547)
        
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
        
    def test_convert_to_self(self):
        same_color = self.color.convert_to('lab')
        self.assertEqual(self.color, same_color)
        
class LuvConversions(unittest.TestCase):
    def setUp(self):
        self.color = LuvColor(1.807, -2.564, -0.894)
        
    def test_conversion_to_xyz(self):
        xyz = self.color.convert_to('xyz')
        self.assertAlmostEqual(xyz.xyz_x, 0.100, 3, "Lab to XYZ failed: X coord")
        self.assertAlmostEqual(xyz.xyz_y, 0.200, 3, "Lab to XYZ failed: Y coord")
        self.assertAlmostEqual(xyz.xyz_z, 0.300, 3, "Lab to XYZ failed: Z coord")
        
    def test_conversion_to_lchuv(self):
        lch = self.color.convert_to('lchuv')
        self.assertAlmostEqual(lch.lch_l, 1.807, 3, "Lab to LCH failed: L coord")
        self.assertAlmostEqual(lch.lch_c, 2.715, 3, "Lab to LCH failed: C coord")
        self.assertAlmostEqual(lch.lch_h, 199.222, 3, "Lab to LCH failed: H coord")
        
    def test_convert_to_self(self):
        same_color = self.color.convert_to('luv')
        self.assertEqual(self.color, same_color)
        
class LCHabConversions(unittest.TestCase):
    def setUp(self):
        self.color = LCHabColor(1.807, 4.532, 214.191)
                
    def test_conversion_to_lab(self):
        lab = self.color.convert_to('lab')
        self.assertAlmostEqual(lab.lab_l, 1.807, 3, "LCHab to Lab failed: L coord")
        self.assertAlmostEqual(lab.lab_a, -3.749, 3, "LCHab to Lab failed: a coord")
        self.assertAlmostEqual(lab.lab_b, -2.547, 3, "LCHab to Lab failed: b coord")
        
    def test_convert_to_self(self):
        same_color = self.color.convert_to('lchab')
        self.assertEqual(self.color, same_color)
        
class LCHuvConversions(unittest.TestCase):
    def setUp(self):
        self.color = LCHuvColor(1.807, 2.715, 199.228)
                
    def test_conversion_to_luv(self):
        luv = self.color.convert_to('luv')
        self.assertAlmostEqual(luv.luv_l, 1.807, 3, "LCHuv to Luv failed: L coord")
        self.assertAlmostEqual(luv.luv_u, -2.564, 3, "LCHuv to Luv failed: u coord")
        self.assertAlmostEqual(luv.luv_v, -0.894, 3, "LCHuv to Luv failed: v coord")
        
    def test_convert_to_self(self):
        same_color = self.color.convert_to('lchuv')
        self.assertEqual(self.color, same_color)
        
class RGBConversions(unittest.TestCase):
    def setUp(self):
        self.color = RGBColor(123, 200, 50, rgb_type='sRGB')
        
    def test_conversion_to_hsl_max_r(self):
        color = RGBColor(255, 123, 50, rgb_type='sRGB')
        hsl = color.convert_to('hsl')
        self.assertAlmostEqual(hsl.hsl_h, 21.366, 3, "RGB R to HSL failed: H coord")
        self.assertAlmostEqual(hsl.hsl_s, 1.000, 3, "RGB R to HSL failed: S coord")
        self.assertAlmostEqual(hsl.hsl_l, 0.598, 3, "RGB R to HSL failed: L coord")
        
    def test_conversion_to_hsl_max_g(self):
        color = RGBColor(123, 255, 50, rgb_type='sRGB')
        hsl = color.convert_to('hsl')
        self.assertAlmostEqual(hsl.hsl_h, 98.634, 3, "RGB G to HSL failed: H coord")
        self.assertAlmostEqual(hsl.hsl_s, 1.000, 3, "RGB G to HSL failed: S coord")
        self.assertAlmostEqual(hsl.hsl_l, 0.598, 3, "RGB G to HSL failed: L coord")
        
    def test_conversion_to_hsl_max_b(self):
        color = RGBColor(123, 123, 255, rgb_type='sRGB')
        hsl = color.convert_to('hsl')
        self.assertAlmostEqual(hsl.hsl_h, 240.000, 3, "RGB B to HSL failed: H coord")
        self.assertAlmostEqual(hsl.hsl_s, 1.000, 3, "RGB B to HSL failed: S coord")
        self.assertAlmostEqual(hsl.hsl_l, 0.741, 3, "RGB B to HSL failed: L coord")
        
    def test_conversion_to_hsl_gray(self):
        color = RGBColor(123, 123, 123, rgb_type='sRGB')
        hsl = color.convert_to('hsl')
        self.assertAlmostEqual(hsl.hsl_h, 0.000, 3, "RGB Gray to HSL failed: H coord")
        self.assertAlmostEqual(hsl.hsl_s, 0.000, 3, "RGB Gray to HSL failed: S coord")
        self.assertAlmostEqual(hsl.hsl_l, 0.482, 3, "RGB Gray to HSL failed: L coord")
                
    def test_conversion_to_cmy(self):
        cmy = self.color.convert_to('cmy')
        self.assertAlmostEqual(cmy.cmy_c, 0.518, 3, "RGB to CMY failed: C coord")
        self.assertAlmostEqual(cmy.cmy_m, 0.216, 3, "RGB to CMY failed: M coord")
        self.assertAlmostEqual(cmy.cmy_y, 0.804, 3, "RGB to CMY failed: Y coord")
        
    def test_srgb_conversion_to_xyz_d50(self):
        """
        sRGB's native illuminant is D65. Test the XYZ adaptations by setting
        a target illuminant to something other than D65.
        """
        xyz = self.color.convert_to('xyz', target_illuminant='D50')
        self.assertAlmostEqual(xyz.xyz_x, 0.313, 3, "RGB to XYZ failed: X coord")
        self.assertAlmostEqual(xyz.xyz_y, 0.460, 3, "RGB to XYZ failed: Y coord")
        self.assertAlmostEqual(xyz.xyz_z, 0.082, 3, "RGB to XYZ failed: Z coord")
        
    def test_srgb_conversion_to_xyz_d65(self):
        """
        sRGB's native illuminant is D65. This is a straightforward conversion.
        """
        xyz = self.color.convert_to('xyz')
        self.assertAlmostEqual(xyz.xyz_x, 0.294, 3, "RGB to XYZ failed: X coord")
        self.assertAlmostEqual(xyz.xyz_y, 0.457, 3, "RGB to XYZ failed: Y coord")
        self.assertAlmostEqual(xyz.xyz_z, 0.103, 3, "RGB to XYZ failed: Z coord")
        
    def test_adobe_conversion_to_xyz_d65(self):
        """
        Adobe RGB's native illuminant is D65, like sRGB's. However, sRGB uses
        different conversion math that uses gamma, so test the alternate logic
        route for non-sRGB RGB colors.
        """
        adobe = RGBColor(123, 200, 50, rgb_type='adobe_rgb')
        xyz = adobe.convert_to('xyz')
        self.assertAlmostEqual(xyz.xyz_x, 0.230, 3, "RGB to XYZ failed: X coord")
        self.assertAlmostEqual(xyz.xyz_y, 0.430, 3, "RGB to XYZ failed: Y coord")
        self.assertAlmostEqual(xyz.xyz_z, 0.074, 3, "RGB to XYZ failed: Z coord")
        
    def test_adobe_conversion_to_xyz_d50(self):
        """
        Adobe RGB's native illuminant is D65, so an adaptation matrix is
        involved here. However, the math for sRGB and all other RGB types is
        different, so test all of the other types with an adaptation matrix
        here.
        """
        adobe = RGBColor(123, 200, 50, rgb_type='adobe_rgb')
        xyz = adobe.convert_to('xyz', target_illuminant='D50')
        self.assertAlmostEqual(xyz.xyz_x, 0.247, 3, "RGB to XYZ failed: X coord")
        self.assertAlmostEqual(xyz.xyz_y, 0.431, 3, "RGB to XYZ failed: Y coord")
        self.assertAlmostEqual(xyz.xyz_z, 0.060, 3, "RGB to XYZ failed: Z coord")
        
    def test_convert_to_self(self):
        same_color = self.color.convert_to('rgb')
        self.assertEqual(self.color, same_color)
        
    def test_get_rgb_hex(self):
        hex_str = self.color.get_rgb_hex()
        self.assertEqual(hex_str, "#7bc832", "RGB to hex conversion failed")
        
    def test_set_from_rgb_hex(self):
        rgb = RGBColor()
        rgb.set_from_rgb_hex('#7bc832')
        self.assertEqual(rgb.rgb_r, 123, "RGB from hex failed: R coord")
        self.assertEqual(rgb.rgb_g, 200, "RGB from hex failed: G coord")
        self.assertEqual(rgb.rgb_b, 50, "RGB from hex failed: B coord")
        
class CMYConversions(unittest.TestCase):
    def setUp(self):
        self.color = CMYColor(0.518, 0.216, 0.804)
                
    def test_conversion_to_cmyk(self):
        cmyk = self.color.convert_to('cmyk')
        self.assertAlmostEqual(cmyk.cmyk_c, 0.385, 3, "CMY to CMYK failed: C coord")
        self.assertAlmostEqual(cmyk.cmyk_m, 0.000, 3, "CMY to CMYK failed: M coord")
        self.assertAlmostEqual(cmyk.cmyk_y, 0.750, 3, "CMY to CMYK failed: Y coord")
        self.assertAlmostEqual(cmyk.cmyk_k, 0.216, 3, "CMY to CMYK failed: K coord")
        
    def test_conversion_to_rgb(self):
        rgb = self.color.convert_to('rgb')
        self.assertEqual(rgb.rgb_r, 123, "CMY to RGB failed: R coord")
        self.assertEqual(rgb.rgb_g, 200, "CMY to RGB failed: G coord")
        self.assertEqual(rgb.rgb_b, 50, "CMY to RGB failed: B coord")
        
    def test_convert_to_self(self):
        same_color = self.color.convert_to('cmy')
        self.assertEqual(self.color, same_color)
        
class CMYKConversions(unittest.TestCase):
    def setUp(self):
        self.color = CMYKColor(0.385, 0.000, 0.750, 0.216)
                
    def test_conversion_to_cmy(self):
        cmy = self.color.convert_to('cmy')
        self.assertAlmostEqual(cmy.cmy_c, 0.518, 3, "CMYK to CMY failed: C coord")
        self.assertAlmostEqual(cmy.cmy_m, 0.216, 3, "CMYK to CMY failed: M coord")
        self.assertAlmostEqual(cmy.cmy_y, 0.804, 3, "CMYK to CMY failed: Y coord")
        
    def test_convert_to_self(self):
        same_color = self.color.convert_to('cmyk')
        self.assertEqual(self.color, same_color)
        
class ValueTests(unittest.TestCase):
    def setUp(self):
        self.color = LabColor(lab_l = 1.807, lab_b = -2.547)
        
    def test_missing_val(self):
        self.color.lab_a = None
        self.assertRaises(MissingValue, self.color.convert_to, 'xyz')
        
    def test_invalid_val(self):
        self.color.lab_a = 'THIS IS NOT A VALID a* COORDINATE'
        self.assertRaises(InvalidValue, self.color.convert_to, 'xyz')
        
    def test_invalid_observer(self):
        self.color.observer = 'THIS IS NOT A VALID OBSERVER ANGLE'
        self.assertRaises(InvalidObserver, self.color.convert_to, 'xyz')

if __name__ == '__main__':
    unittest.main()