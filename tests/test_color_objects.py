"""
Various tests for color objects.
"""

import unittest

from colormath.color_conversions import convert_color
from colormath.color_objects import SpectralColor, XYZColor, xyYColor, \
    LabColor, LuvColor, LCHabColor, LCHuvColor, RGBColor, HSLColor, HSVColor, \
    CMYColor, CMYKColor


class BaseColorConversionTest(unittest.TestCase):
    """
    All color conversion tests should inherit from this class. Has some
    convenience methods for re-use.
    """

    # noinspection PyPep8Naming
    def assertColorMatch(self, conv, std):
        """
        Checks a converted color against an expected standard.

        :param conv: The converted color object.
        :param std: The object to use as a standard for comparison.
        """

        self.assertEqual(conv.__class__, std.__class__)
        attribs = std.VALUES
        for attrib in attribs:
            conv_value = getattr(conv, attrib)
            std_value = getattr(std, attrib)
            self.assertAlmostEqual(
                conv_value, std_value, 3,
                "%s is %s, expected %s" % (attrib, conv_value, std_value))


class SpectralConversionTestCase(BaseColorConversionTest):
    def setUp(self):
        """
        While it is possible to specify the entire spectral color using
        positional arguments, set this thing up with keywords for the ease of
        manipulation.
        """

        color = SpectralColor(
            spec_380nm=0.0600, spec_390nm=0.0600, spec_400nm=0.0641,
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
        xyz = convert_color(self.color, XYZColor)
        self.assertColorMatch(xyz, XYZColor(0.115, 0.099, 0.047))

    def test_conversion_to_xyz_with_negatives(self):
        """
        This has negative spectral values, which should never happen. Just
        clamp these to 0.0 instead of running into the domain errors. A badly
        or uncalibrated spectro can sometimes report negative values.
        """

        self.color.spec_530nm = -0.0736
        # TODO: Convert here.

    def test_convert_to_self(self):
        same_color = convert_color(self.color, SpectralColor)
        self.assertEqual(self.color, same_color)


class XYZConversionTestCase(BaseColorConversionTest):
    def setUp(self):
        self.color = XYZColor(0.1, 0.2, 0.3)

    def test_conversion_to_xyy(self):
        xyy = convert_color(self.color, xyYColor)
        self.assertColorMatch(xyy, xyYColor(0.167, 0.333, 0.200))

    def test_conversion_to_lab(self):
        lab = convert_color(self.color, LabColor)
        self.assertColorMatch(lab, LabColor(51.837, -57.486, -25.780))

    def test_conversion_to_rgb(self):
        # Picked a set of XYZ coordinates that would return a good RGB value.
        self.color = XYZColor(0.300, 0.200, 0.300)
        rgb = convert_color(self.color, RGBColor)
        self.assertColorMatch(rgb, RGBColor(0.715, 0.349, 0.663))

    def test_conversion_to_luv(self):
        luv = convert_color(self.color, LuvColor)
        self.assertColorMatch(luv, LuvColor(51.837, -73.561, -25.657))

    def test_convert_to_self(self):
        same_color = convert_color(self.color, XYZColor)
        self.assertEqual(self.color, same_color)


# noinspection PyPep8Naming
class xyYConversionTestCase(BaseColorConversionTest):
    def setUp(self):
        self.color = xyYColor(0.167, 0.333, 0.200)

    def test_conversion_to_xyz(self):
        xyz = convert_color(self.color, XYZColor)
        self.assertColorMatch(xyz, XYZColor(0.100, 0.200, 0.300))

    def test_convert_to_self(self):
        same_color = convert_color(self.color, xyYColor)
        self.assertEqual(self.color, same_color)


class LabConversionTestCase(BaseColorConversionTest):
    def setUp(self):
        self.color = LabColor(1.807, -3.749, -2.547)

    def test_conversion_to_xyz(self):
        xyz = convert_color(self.color, XYZColor)
        self.assertColorMatch(xyz, XYZColor(0.001, 0.002, 0.003))

    def test_conversion_to_lchab(self):
        lch = convert_color(self.color, LCHabColor)
        self.assertColorMatch(lch, LCHabColor(1.807, 4.532, 214.191))

    def test_convert_to_self(self):
        same_color = convert_color(self.color, LabColor)
        self.assertEqual(self.color, same_color)


class LuvConversionTestCase(BaseColorConversionTest):
    def setUp(self):
        self.color = LuvColor(1.807, -2.564, -0.894)

    def test_conversion_to_xyz(self):
        xyz = convert_color(self.color, XYZColor)
        self.assertColorMatch(xyz, XYZColor(0.001, 0.002, 0.003))

    def test_conversion_to_lchuv(self):
        lch = convert_color(self.color, LCHuvColor)
        self.assertColorMatch(lch, LCHuvColor(1.807, 2.715, 199.222))

    def test_convert_to_self(self):
        same_color = convert_color(self.color, LuvColor)
        self.assertEqual(self.color, same_color)


class LCHabConversionTestCase(BaseColorConversionTest):
    def setUp(self):
        self.color = LCHabColor(1.807, 4.532, 214.191)

    def test_conversion_to_lab(self):
        lab = convert_color(self.color, LabColor)
        self.assertColorMatch(lab, LabColor(1.807, -3.749, -2.547))

    def test_conversion_to_rgb_zero_div(self):
        """
        The formula I grabbed for LCHuv to XYZ had a zero division error in it
        if the L coord was 0. Also check against LCHab in case.

        Issue #13 in the Google Code tracker.
        """

        lchab = LCHabColor(0.0, 0.0, 0.0)
        rgb = convert_color(lchab, RGBColor)
        self.assertColorMatch(rgb, RGBColor(0.0, 0.0, 0.0))

    def test_convert_to_self(self):
        same_color = convert_color(self.color, LCHabColor)
        self.assertEqual(self.color, same_color)


class LCHuvConversionTestCase(BaseColorConversionTest):
    def setUp(self):
        self.color = LCHuvColor(1.807, 2.715, 199.228)

    def test_conversion_to_luv(self):
        luv = convert_color(self.color, LuvColor)
        self.assertColorMatch(luv, LuvColor(1.807, -2.564, -0.894))

    def test_conversion_to_rgb_zero_div(self):
        """
        The formula I grabbed for LCHuv to XYZ had a zero division error in it
        if the L coord was 0. Check against that here.

        Issue #13 in the Google Code tracker.
        """

        lchuv = LCHuvColor(0.0, 0.0, 0.0)
        rgb = convert_color(lchuv, RGBColor)
        self.assertColorMatch(rgb, RGBColor(0.0, 0.0, 0.0))

    def test_convert_to_self(self):
        same_color = convert_color(self.color, LCHuvColor)
        self.assertEqual(self.color, same_color)


class RGBConversionTestCase(BaseColorConversionTest):
    def setUp(self):
        self.color = RGBColor(0.482, 0.784, 0.196, rgb_type='sRGB')

    def test_to_xyz_and_back(self):
        xyz = convert_color(self.color, XYZColor)
        rgb = convert_color(xyz, RGBColor)
        self.assertColorMatch(rgb, self.color)

    def test_conversion_to_hsl_max_r(self):
        color = RGBColor(255, 123, 50, rgb_type='sRGB', is_upscaled=True)
        hsl = convert_color(color, HSLColor)
        self.assertColorMatch(hsl, HSLColor(21.366, 1.000, 0.598))

    def test_conversion_to_hsl_max_g(self):
        color = RGBColor(123, 255, 50, rgb_type='sRGB', is_upscaled=True)
        hsl = convert_color(color, HSLColor)
        self.assertColorMatch(hsl, HSLColor(98.634, 1.000, 0.598))

    def test_conversion_to_hsl_max_b(self):
        color = RGBColor(0.482, 0.482, 1.0, rgb_type='sRGB')
        hsl = convert_color(color, HSLColor)
        self.assertColorMatch(hsl, HSLColor(240.000, 1.000, 0.741))

    def test_conversion_to_hsl_gray(self):
        color = RGBColor(0.482, 0.482, 0.482, rgb_type='sRGB')
        hsl = convert_color(color, HSLColor)
        self.assertColorMatch(hsl, HSLColor(0.000, 0.000, 0.482))

    def test_conversion_to_hsv(self):
        hsv = convert_color(self.color, HSVColor)
        self.assertColorMatch(hsv, HSVColor(90.816, 0.750, 0.784))

    def test_conversion_to_cmy(self):
        cmy = convert_color(self.color, CMYColor)
        self.assertColorMatch(cmy, CMYColor(0.518, 0.216, 0.804))

    def test_srgb_conversion_to_xyz_d50(self):
        """
        sRGB's native illuminant is D65. Test the XYZ adaptations by setting
        a target illuminant to something other than D65.
        """

        xyz = convert_color(self.color, XYZColor, target_illuminant='D50')
        self.assertColorMatch(xyz, XYZColor(0.313, 0.460, 0.082))

    def test_srgb_conversion_to_xyz_d65(self):
        """
        sRGB's native illuminant is D65. This is a straightforward conversion.
        """

        xyz = convert_color(self.color, XYZColor)
        self.assertColorMatch(xyz, XYZColor(0.294, 0.457, 0.103))

    def test_adobe_conversion_to_xyz_d65(self):
        """
        Adobe RGB's native illuminant is D65, like sRGB's. However, sRGB uses
        different conversion math that uses gamma, so test the alternate logic
        route for non-sRGB RGB colors.
        """
        adobe = RGBColor(0.482, 0.784, 0.196, rgb_type='adobe_rgb')
        xyz = convert_color(adobe, XYZColor)
        self.assertColorMatch(xyz, XYZColor(0.230, 0.429, 0.074))

    def test_adobe_conversion_to_xyz_d50(self):
        """
        Adobe RGB's native illuminant is D65, so an adaptation matrix is
        involved here. However, the math for sRGB and all other RGB types is
        different, so test all of the other types with an adaptation matrix
        here.
        """
        adobe = RGBColor(0.482, 0.784, 0.196, rgb_type='adobe_rgb')
        xyz = convert_color(adobe, XYZColor, target_illuminant='D50')
        self.assertColorMatch(xyz, XYZColor(0.247, 0.431, 0.060))

    def test_convert_to_self(self):
        same_color = convert_color(self.color, RGBColor)
        self.assertEqual(self.color, same_color)

    def test_get_rgb_hex(self):
        hex_str = self.color.get_rgb_hex()
        self.assertEqual(hex_str, "#7bc832", "sRGB to hex conversion failed")

    def test_set_from_rgb_hex(self):
        rgb = RGBColor.new_from_rgb_hex('#7bc832')
        self.assertColorMatch(rgb, RGBColor(0.482, 0.784, 0.196))


class HSLConversionTestCase(BaseColorConversionTest):
    def setUp(self):
        self.color = HSLColor(200.0, 0.400, 0.500)

    def test_conversion_to_rgb(self):
        rgb = convert_color(self.color, RGBColor)
        self.assertColorMatch(rgb, RGBColor(0.300, 0.567, 0.700))

    def test_convert_to_self(self):
        same_color = convert_color(self.color, HSLColor)
        self.assertEqual(self.color, same_color)


class HSVConversionTestCase(BaseColorConversionTest):
    def setUp(self):
        self.color = HSVColor(91.0, 0.750, 0.784)

    def test_conversion_to_rgb(self):
        rgb = convert_color(self.color, RGBColor)
        self.assertColorMatch(rgb, RGBColor(0.480, 0.784, 0.196))

    def test_convert_to_self(self):
        same_color = convert_color(self.color, HSVColor)
        self.assertEqual(self.color, same_color)


class CMYConversionTestCase(BaseColorConversionTest):
    def setUp(self):
        self.color = CMYColor(0.518, 0.216, 0.804)

    def test_conversion_to_cmyk(self):
        cmyk = convert_color(self.color, CMYKColor)
        self.assertColorMatch(cmyk, CMYKColor(0.385, 0.000, 0.750, 0.216))

    def test_conversion_to_rgb(self):
        rgb = convert_color(self.color, RGBColor)
        self.assertColorMatch(rgb, RGBColor(0.482, 0.784, 0.196))

    def test_convert_to_self(self):
        same_color = convert_color(self.color, CMYColor)
        self.assertEqual(self.color, same_color)


class CMYKConversionTestCase(BaseColorConversionTest):
    def setUp(self):
        self.color = CMYKColor(0.385, 0.000, 0.750, 0.216)

    def test_conversion_to_cmy(self):
        cmy = convert_color(self.color, CMYColor)
        self.assertColorMatch(cmy, CMYColor(0.518, 0.216, 0.804))

    def test_convert_to_self(self):
        same_color = convert_color(self.color, CMYKColor)
        self.assertEqual(self.color, same_color)
