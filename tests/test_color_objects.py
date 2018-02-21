# -*- coding: utf-8 -*-
"""
Various tests for color objects.
"""

import unittest

from colormath.color_conversions import convert_color
from colormath.color_objects import SpectralColor, XYZColor, xyYColor, \
    LabColor, LuvColor, LCHabColor, LCHuvColor, sRGBColor, HSLColor, HSVColor, \
    CMYColor, CMYKColor, AdobeRGBColor, AppleRGBColor, IPTColor


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
        rgb = convert_color(self.color, sRGBColor)
        self.assertColorMatch(rgb, sRGBColor(0.715, 0.349, 0.663))

    def test_conversion_to_apple_rgb(self):
        self.color = XYZColor(0.0157, 0.0191, 0.0331)
        rgb = convert_color(self.color, AppleRGBColor)
        self.assertColorMatch(rgb, AppleRGBColor(0.0411, 0.1214, 0.1763))

    def test_conversion_to_adobe_rgb(self):
        self.color = XYZColor(0.2553, 0.1125, 0.0011)
        rgb = convert_color(self.color, AdobeRGBColor)
        # This ends up getting clamped.
        self.assertColorMatch(rgb, AdobeRGBColor(0.6828, 0.0, 0.0))

    def test_conversion_to_luv(self):
        luv = convert_color(self.color, LuvColor)
        self.assertColorMatch(luv, LuvColor(51.837, -73.561, -25.657))

    def test_conversion_to_ipt(self):
        self.color.set_illuminant('D65')
        ipt = convert_color(self.color, IPTColor)
        self.assertColorMatch(ipt, IPTColor(0.5063, -0.3183, -0.1160))

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


# noinspection PyAttributeOutsideInit,PyPep8Naming
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
        """

        lchab = LCHabColor(0.0, 0.0, 0.0)
        rgb = convert_color(lchab, sRGBColor)
        self.assertColorMatch(rgb, sRGBColor(0.0, 0.0, 0.0))

    def test_to_rgb_domain_error(self):
        """
        Tests for a bug resulting in a domain error with LCH->Adobe RGB.

        See: https://github.com/gtaylor/python-colormath/issues/49
        """

        lchab = LCHabColor(40.0, 104.0, 40.0)
        _rgb = convert_color(lchab, AdobeRGBColor)

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
        rgb = convert_color(lchuv, sRGBColor)
        self.assertColorMatch(rgb, sRGBColor(0.0, 0.0, 0.0))

    def test_convert_to_self(self):
        same_color = convert_color(self.color, LCHuvColor)
        self.assertEqual(self.color, same_color)


class RGBConversionTestCase(BaseColorConversionTest):
    def setUp(self):
        self.color = sRGBColor(0.482, 0.784, 0.196)

    def test_channel_clamping(self):
        high_r = sRGBColor(1.482, 0.2, 0.3)
        self.assertEqual(high_r.clamped_rgb_r, 1.0)
        self.assertEqual(high_r.clamped_rgb_g, high_r.rgb_g)
        self.assertEqual(high_r.clamped_rgb_b, high_r.rgb_b)

        low_r = sRGBColor(-0.1, 0.2, 0.3)
        self.assertEqual(low_r.clamped_rgb_r, 0.0)
        self.assertEqual(low_r.clamped_rgb_g, low_r.rgb_g)
        self.assertEqual(low_r.clamped_rgb_b, low_r.rgb_b)

        high_g = sRGBColor(0.2, 1.482, 0.3)
        self.assertEqual(high_g.clamped_rgb_r, high_g.rgb_r)
        self.assertEqual(high_g.clamped_rgb_g, 1.0)
        self.assertEqual(high_g.clamped_rgb_b, high_g.rgb_b)

        low_g = sRGBColor(0.2, -0.1, 0.3)
        self.assertEqual(low_g.clamped_rgb_r, low_g.rgb_r)
        self.assertEqual(low_g.clamped_rgb_g, 0.0)
        self.assertEqual(low_g.clamped_rgb_b, low_g.rgb_b)

        high_b = sRGBColor(0.1, 0.2, 1.482)
        self.assertEqual(high_b.clamped_rgb_r, high_b.rgb_r)
        self.assertEqual(high_b.clamped_rgb_g, high_b.rgb_g)
        self.assertEqual(high_b.clamped_rgb_b, 1.0)

        low_b = sRGBColor(0.1, 0.2, -0.1)
        self.assertEqual(low_b.clamped_rgb_r, low_b.rgb_r)
        self.assertEqual(low_b.clamped_rgb_g, low_b.rgb_g)
        self.assertEqual(low_b.clamped_rgb_b, 0.0)

    def test_to_xyz_and_back(self):
        xyz = convert_color(self.color, XYZColor)
        rgb = convert_color(xyz, sRGBColor)
        self.assertColorMatch(rgb, self.color)

    def test_conversion_to_hsl_max_r(self):
        color = sRGBColor(255, 123, 50, is_upscaled=True)
        hsl = convert_color(color, HSLColor)
        self.assertColorMatch(hsl, HSLColor(21.366, 1.000, 0.598))

    def test_conversion_to_hsl_max_g(self):
        color = sRGBColor(123, 255, 50, is_upscaled=True)
        hsl = convert_color(color, HSLColor)
        self.assertColorMatch(hsl, HSLColor(98.634, 1.000, 0.598))

    def test_conversion_to_hsl_max_b(self):
        color = sRGBColor(0.482, 0.482, 1.0)
        hsl = convert_color(color, HSLColor)
        self.assertColorMatch(hsl, HSLColor(240.000, 1.000, 0.741))

    def test_conversion_to_hsl_gray(self):
        color = sRGBColor(0.482, 0.482, 0.482)
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

        adobe = AdobeRGBColor(0.482, 0.784, 0.196)
        xyz = convert_color(adobe, XYZColor)
        self.assertColorMatch(xyz, XYZColor(0.230, 0.429, 0.074))

    def test_conversion_through_rgb(self):
        """
        Make sure our convenience RGB tracking feature is working. For example,
        going from XYZ->HSL via Adobe RGB, then taking that HSL object and
        converting back to XYZ should also use Adobe RGB (instead of the
        default of sRGB).
        """

        xyz = convert_color(self.color, XYZColor)
        hsl = convert_color(xyz, HSLColor, through_rgb_type=AdobeRGBColor)
        # Notice how we don't have to pass through_rgb_type explicitly.
        xyz2 = convert_color(hsl, XYZColor)
        self.assertColorMatch(xyz, xyz2)

    def test_adobe_conversion_to_xyz_d50(self):
        """
        Adobe RGB's native illuminant is D65, so an adaptation matrix is
        involved here. However, the math for sRGB and all other RGB types is
        different, so test all of the other types with an adaptation matrix
        here.
        """

        adobe = AdobeRGBColor(0.482, 0.784, 0.196)
        xyz = convert_color(adobe, XYZColor, target_illuminant='D50')
        self.assertColorMatch(xyz, XYZColor(0.247, 0.431, 0.060))

    def test_convert_to_self(self):
        same_color = convert_color(self.color, sRGBColor)
        self.assertEqual(self.color, same_color)

    def test_get_rgb_hex(self):
        hex_str = self.color.get_rgb_hex()
        self.assertEqual(hex_str, "#7bc832", "sRGB to hex conversion failed")

    def test_set_from_rgb_hex(self):
        rgb = sRGBColor.new_from_rgb_hex('#7bc832')
        self.assertColorMatch(rgb, sRGBColor(0.482, 0.784, 0.196))


class HSLConversionTestCase(BaseColorConversionTest):
    def setUp(self):
        self.color = HSLColor(200.0, 0.400, 0.500)

    def test_conversion_to_rgb(self):
        rgb = convert_color(self.color, sRGBColor)
        self.assertColorMatch(rgb, sRGBColor(0.300, 0.567, 0.700))
        # Make sure this converts to AdobeRGBColor instead of sRGBColor.
        adobe_rgb = convert_color(self.color, AdobeRGBColor)
        self.assertIsInstance(adobe_rgb, AdobeRGBColor)

    def test_convert_to_self(self):
        same_color = convert_color(self.color, HSLColor)
        self.assertEqual(self.color, same_color)


class HSVConversionTestCase(BaseColorConversionTest):
    def setUp(self):
        self.color = HSVColor(91.0, 0.750, 0.784)

    def test_conversion_to_rgb(self):
        rgb = convert_color(self.color, sRGBColor)
        self.assertColorMatch(rgb, sRGBColor(0.480, 0.784, 0.196))

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
        rgb = convert_color(self.color, sRGBColor)
        self.assertColorMatch(rgb, sRGBColor(0.482, 0.784, 0.196))

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


class IPTConversionTestCase(BaseColorConversionTest):
    def setUp(self):
        self.color = IPTColor(0.5, 0.5, 0.5)

    def test_convert_so_self(self):
        same_color = convert_color(self.color, IPTColor)
        self.assertEqual(self.color, same_color)

    def test_convert_to_XYZ(self):
        xyz = convert_color(self.color, XYZColor)
        self.assertColorMatch(xyz, XYZColor(0.4497, 0.2694, 0.0196, illuminant='d65', observer='2'))

    def test_consistency(self):
        xyz = convert_color(self.color, XYZColor)
        same_color = convert_color(xyz, IPTColor)
        self.assertColorMatch(self.color, same_color)

    def test_illuminant_guard(self):
        xyz = XYZColor(1, 1, 1, illuminant='d50', observer='2')
        ipt_conversion = lambda: convert_color(xyz, IPTColor)
        self.assertRaises(ValueError, ipt_conversion)

    def test_observer_guard(self):
        xyz = XYZColor(1, 1, 1, illuminant='d65', observer='10')
        ipt_conversion = lambda: convert_color(xyz, IPTColor)
        self.assertRaises(ValueError, ipt_conversion)

