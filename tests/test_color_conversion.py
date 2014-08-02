import itertools
import unittest
from colormath import color_conversions
from colormath.color_conversions import GraphConversionManager, XYZ_to_RGB, RGB_to_HSV, HSV_to_RGB
from colormath.color_exceptions import UndefinedConversionError
from colormath.color_objects import XYZColor, BaseRGBColor, HSVColor, HSLColor


class GraphConversionManagerTestCase(unittest.TestCase):
    def setUp(self):
        self.manager = GraphConversionManager()
        self.manager.add_type_conversion(XYZColor, BaseRGBColor, XYZ_to_RGB)
        self.manager.add_type_conversion(BaseRGBColor, HSVColor, HSV_to_RGB)

    def test_basic_path_generation(self):
        path = self.manager.get_conversion_path(XYZColor, HSVColor)
        self.assertEqual(path, [XYZ_to_RGB, HSV_to_RGB])

    def test_self_conversion(self):
        path = self.manager.get_conversion_path(XYZColor, XYZColor)
        self.assertEqual(path, [])

    def test_invalid_path_response(self):
        self.assertRaises(UndefinedConversionError,
                          self.manager.get_conversion_path,
                          XYZColor, HSLColor
        )


class ColorConversionTestCase(unittest.TestCase):
    def test_conversion_validity(self):
        """
        Make sure that all existing paths between colors are valid.
        """

        conversion_manager = color_conversions._conversion_manager
        color_spaces = conversion_manager.registered_color_spaces

        for start_space, target_space in itertools.product(color_spaces, repeat=2):
            try:
                path = conversion_manager.get_conversion_path(start_space, target_space)
            except UndefinedConversionError:
                # If there is no path we don't really care (e.g., conversion to SpectralColor).
                continue

            if start_space == target_space:
                # If start and end color space are equal, the conversion path should be empty.
                self.assertEqual(path, [])
                continue
            else:
                # Otherwise check that all the conversion functions math up
                for a, b in zip(path[:-1], path[1:]):
                    self.assertEqual(a.target_type, b.start_type)
