"""
Conversion between color spaces.

.. note:: This module makes extensive use of imports within functions.
    That stinks.
"""
from abc import ABCMeta, abstractmethod

import math
import logging

import numpy
import networkx

from colormath import color_constants
from colormath import spectral_constants
from colormath.color_objects import ColorBase, XYZColor, sRGBColor, \
    LCHabColor, LCHuvColor, LabColor, xyYColor, LuvColor, HSVColor, HSLColor, \
    CMYColor, CMYKColor, BaseRGBColor, IPTColor, SpectralColor, AdobeRGBColor
from colormath.chromatic_adaptation import apply_chromatic_adaptation
from colormath.color_exceptions import InvalidIlluminantError, \
    UndefinedConversionError


logger = logging.getLogger(__name__)


# noinspection PyPep8Naming
def apply_RGB_matrix(var1, var2, var3, rgb_type, convtype="xyz_to_rgb"):
    """
    Applies an RGB working matrix to convert from XYZ to RGB.
    The arguments are tersely named var1, var2, and var3 to allow for the
    passing of XYZ _or_ RGB values. var1 is X for XYZ, and R for RGB. var2 and
    var3 follow suite.
    """
    convtype = convtype.lower()
    # Retrieve the appropriate transformation matrix from the constants.
    rgb_matrix = rgb_type.conversion_matrices[convtype]

    logger.debug("  \* Applying RGB conversion matrix: %s->%s",
                 rgb_type.__class__.__name__, convtype)
    # Stuff the RGB/XYZ values into a NumPy matrix for conversion.
    var_matrix = numpy.array((
        var1, var2, var3
    ))
    # Perform the adaptation via matrix multiplication.
    result_matrix = numpy.dot(rgb_matrix, var_matrix)
    rgb_r, rgb_g, rgb_b = result_matrix
    # Clamp these values to a valid range.
    rgb_r = max(rgb_r, 0.0)
    rgb_g = max(rgb_g, 0.0)
    rgb_b = max(rgb_b, 0.0)
    return rgb_r, rgb_g, rgb_b


# Avoid the repetition, since the conversion tables for the various RGB
# spaces are the same.
_RGB_SPACES = [sRGBColor, AdobeRGBColor]


class ConversionManager(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self.registered_color_spaces = set()

    def add_type_conversion(self, start_type, target_type, conversion_function):
        """
        Register a conversion function between two color spaces.
        :param start_type: Starting color space.
        :param target_type: Target color space.
        :param conversion_function: Conversion function.
        """
        self.registered_color_spaces.add(start_type)
        self.registered_color_spaces.add(target_type)
        logger.debug(
            'Registered conversion from %s to %s', start_type, target_type)

    @abstractmethod
    def get_conversion_path(self, start_type, target_type):
        """
        Return a list of conversion functions that if applied iteratively on a
        color of the start_type color space result in a color in the result_type
        color space.

        Raises an UndefinedConversionError if no valid conversion path
        can be found.

        :param start_type: Starting color space type.
        :param target_type: Target color space type.
        :return: List of conversion functions.
        """
        pass

    @staticmethod
    def _normalise_type(color_type):
        """
        Return the highest superclass that is valid for color space
        conversions (e.g., AdobeRGB -> BaseRGBColor).
        """
        if issubclass(color_type, BaseRGBColor):
            return BaseRGBColor
        else:
            return color_type


class GraphConversionManager(ConversionManager):
    def __init__(self):
        super(GraphConversionManager, self).__init__()
        self.conversion_graph = networkx.DiGraph()

    def get_conversion_path(self, start_type, target_type):
        start_type = self._normalise_type(start_type)
        target_type = self._normalise_type(target_type)
        try:
            # Retrieve node sequence that leads from start_type to target_type.
            return self._find_shortest_path(start_type, target_type)
        except (networkx.NetworkXNoPath, networkx.NodeNotFound):
            raise UndefinedConversionError(
                start_type,
                target_type,
            )

    def _find_shortest_path(self, start_type, target_type):
        path = networkx.shortest_path(
            self.conversion_graph, start_type, target_type)
        # Look up edges between nodes and retrieve the conversion function
        # for each edge.
        return [
            self.conversion_graph.get_edge_data(node_a, node_b)['conversion_function']
            for node_a, node_b in zip(path[:-1], path[1:])
        ]

    def add_type_conversion(self, start_type, target_type, conversion_function):
        super(GraphConversionManager, self).add_type_conversion(
            start_type, target_type, conversion_function)
        self.conversion_graph.add_edge(
            start_type, target_type, conversion_function=conversion_function)


class DummyConversionManager(ConversionManager):
    def add_type_conversion(self, start_type, target_type, conversion_function):
        pass

    def get_conversion_path(self, start_type, target_type):
        raise UndefinedConversionError(
            start_type,
            target_type,
        )


_conversion_manager = GraphConversionManager()


def color_conversion_function(start_type, target_type):
    """
    Decorator to indicate a function that performs a conversion from one color
    space to another.

    This decorator will return the original function unmodified, however it will
    be registered in the _conversion_manager so it can be used to perform color
    space transformations between color spaces that do not have direct
    conversion functions (e.g., Luv to CMYK).

    Note: For a conversion to/from RGB supply the BaseRGBColor class.

    :param start_type: Starting color space type
    :param target_type: Target color space type
    """
    def decorator(f):
        f.start_type = start_type
        f.target_type = target_type
        _conversion_manager.add_type_conversion(start_type, target_type, f)
        return f

    return decorator


# noinspection PyPep8Naming,PyUnusedLocal
@color_conversion_function(SpectralColor, XYZColor)
def Spectral_to_XYZ(cobj, illuminant_override=None, *args, **kwargs):
    """
    Converts spectral readings to XYZ.
    """
    # If the user provides an illuminant_override numpy array, use it.
    if illuminant_override:
        reference_illum = illuminant_override
    else:
        # Otherwise, look up the illuminant from known standards based
        # on the value of 'illuminant' pulled from the SpectralColor object.
        try:
            reference_illum = spectral_constants.REF_ILLUM_TABLE[cobj.illuminant]
        except KeyError:
            raise InvalidIlluminantError(cobj.illuminant)

    # Get the spectral distribution of the selected standard observer.
    if cobj.observer == '10':
        std_obs_x = spectral_constants.STDOBSERV_X10
        std_obs_y = spectral_constants.STDOBSERV_Y10
        std_obs_z = spectral_constants.STDOBSERV_Z10
    else:
        # Assume 2 degree, since it is theoretically the only other possibility.
        std_obs_x = spectral_constants.STDOBSERV_X2
        std_obs_y = spectral_constants.STDOBSERV_Y2
        std_obs_z = spectral_constants.STDOBSERV_Z2

    # This is a NumPy array containing the spectral distribution of the color.
    sample = cobj.get_numpy_array()

    # The denominator is constant throughout the entire calculation for X,
    # Y, and Z coordinates. Calculate it once and re-use.
    denom = std_obs_y * reference_illum

    # This is also a common element in the calculation whereby the sample
    # NumPy array is multiplied by the reference illuminant's power distribution
    # (which is also a NumPy array).
    sample_by_ref_illum = sample * reference_illum

    # Calculate the numerator of the equation to find X.
    x_numerator = sample_by_ref_illum * std_obs_x
    y_numerator = sample_by_ref_illum * std_obs_y
    z_numerator = sample_by_ref_illum * std_obs_z

    xyz_x = x_numerator.sum() / denom.sum()
    xyz_y = y_numerator.sum() / denom.sum()
    xyz_z = z_numerator.sum() / denom.sum()

    return XYZColor(
        xyz_x, xyz_y, xyz_z, observer=cobj.observer, illuminant=cobj.illuminant)


# noinspection PyPep8Naming,PyUnusedLocal
@color_conversion_function(LabColor, LCHabColor)
def Lab_to_LCHab(cobj, *args, **kwargs):
    """
    Convert from CIE Lab to LCH(ab).
    """
    lch_l = cobj.lab_l
    lch_c = math.sqrt(
        math.pow(float(cobj.lab_a), 2) + math.pow(float(cobj.lab_b), 2))
    lch_h = math.atan2(float(cobj.lab_b), float(cobj.lab_a))

    if lch_h > 0:
        lch_h = (lch_h / math.pi) * 180
    else:
        lch_h = 360 - (math.fabs(lch_h) / math.pi) * 180

    return LCHabColor(
        lch_l, lch_c, lch_h, observer=cobj.observer, illuminant=cobj.illuminant)


# noinspection PyPep8Naming,PyUnusedLocal
@color_conversion_function(LabColor, XYZColor)
def Lab_to_XYZ(cobj, *args, **kwargs):
    """
    Convert from Lab to XYZ
    """
    illum = cobj.get_illuminant_xyz()
    xyz_y = (cobj.lab_l + 16.0) / 116.0
    xyz_x = cobj.lab_a / 500.0 + xyz_y
    xyz_z = xyz_y - cobj.lab_b / 200.0

    if math.pow(xyz_y, 3) > color_constants.CIE_E:
        xyz_y = math.pow(xyz_y, 3)
    else:
        xyz_y = (xyz_y - 16.0 / 116.0) / 7.787

    if math.pow(xyz_x, 3) > color_constants.CIE_E:
        xyz_x = math.pow(xyz_x, 3)
    else:
        xyz_x = (xyz_x - 16.0 / 116.0) / 7.787

    if math.pow(xyz_z, 3) > color_constants.CIE_E:
        xyz_z = math.pow(xyz_z, 3)
    else:
        xyz_z = (xyz_z - 16.0 / 116.0) / 7.787

    xyz_x = (illum["X"] * xyz_x)
    xyz_y = (illum["Y"] * xyz_y)
    xyz_z = (illum["Z"] * xyz_z)

    return XYZColor(
        xyz_x, xyz_y, xyz_z, observer=cobj.observer, illuminant=cobj.illuminant)


# noinspection PyPep8Naming,PyUnusedLocal
@color_conversion_function(LuvColor, LCHuvColor)
def Luv_to_LCHuv(cobj, *args, **kwargs):
    """
    Convert from CIE Luv to LCH(uv).
    """
    lch_l = cobj.luv_l
    lch_c = math.sqrt(math.pow(cobj.luv_u, 2.0) + math.pow(cobj.luv_v, 2.0))
    lch_h = math.atan2(float(cobj.luv_v), float(cobj.luv_u))

    if lch_h > 0:
        lch_h = (lch_h / math.pi) * 180
    else:
        lch_h = 360 - (math.fabs(lch_h) / math.pi) * 180
    return LCHuvColor(
        lch_l, lch_c, lch_h, observer=cobj.observer, illuminant=cobj.illuminant)


# noinspection PyPep8Naming,PyUnusedLocal
@color_conversion_function(LuvColor, XYZColor)
def Luv_to_XYZ(cobj, *args, **kwargs):
    """
    Convert from Luv to XYZ.
    """
    illum = cobj.get_illuminant_xyz()
    # Without Light, there is no color. Short-circuit this and avoid some
    # zero division errors in the var_a_frac calculation.
    if cobj.luv_l <= 0.0:
        xyz_x = 0.0
        xyz_y = 0.0
        xyz_z = 0.0
        return XYZColor(
            xyz_x, xyz_y, xyz_z,
            observer=cobj.observer, illuminant=cobj.illuminant)

    # Various variables used throughout the conversion.
    cie_k_times_e = color_constants.CIE_K * color_constants.CIE_E
    u_sub_0 = (4.0 * illum["X"]) / (illum["X"] + 15.0 * illum["Y"] + 3.0 * illum["Z"])
    v_sub_0 = (9.0 * illum["Y"]) / (illum["X"] + 15.0 * illum["Y"] + 3.0 * illum["Z"])
    var_u = cobj.luv_u / (13.0 * cobj.luv_l) + u_sub_0
    var_v = cobj.luv_v / (13.0 * cobj.luv_l) + v_sub_0

    # Y-coordinate calculations.
    if cobj.luv_l > cie_k_times_e:
        xyz_y = math.pow((cobj.luv_l + 16.0) / 116.0, 3.0)
    else:
        xyz_y = cobj.luv_l / color_constants.CIE_K

    # X-coordinate calculation.
    xyz_x = xyz_y * 9.0 * var_u / (4.0 * var_v)
    # Z-coordinate calculation.
    xyz_z = xyz_y * (12.0 - 3.0 * var_u - 20.0 * var_v) / (4.0 * var_v)

    return XYZColor(
        xyz_x, xyz_y, xyz_z, illuminant=cobj.illuminant, observer=cobj.observer)


# noinspection PyPep8Naming,PyUnusedLocal
@color_conversion_function(LCHabColor, LabColor)
def LCHab_to_Lab(cobj, *args, **kwargs):
    """
    Convert from LCH(ab) to Lab.
    """
    lab_l = cobj.lch_l
    lab_a = math.cos(math.radians(cobj.lch_h)) * cobj.lch_c
    lab_b = math.sin(math.radians(cobj.lch_h)) * cobj.lch_c
    return LabColor(
        lab_l, lab_a, lab_b, illuminant=cobj.illuminant, observer=cobj.observer)


# noinspection PyPep8Naming,PyUnusedLocal
@color_conversion_function(LCHuvColor, LuvColor)
def LCHuv_to_Luv(cobj, *args, **kwargs):
    """
    Convert from LCH(uv) to Luv.
    """
    luv_l = cobj.lch_l
    luv_u = math.cos(math.radians(cobj.lch_h)) * cobj.lch_c
    luv_v = math.sin(math.radians(cobj.lch_h)) * cobj.lch_c
    return LuvColor(
        luv_l, luv_u, luv_v, illuminant=cobj.illuminant, observer=cobj.observer)


# noinspection PyPep8Naming,PyUnusedLocal
@color_conversion_function(xyYColor, XYZColor)
def xyY_to_XYZ(cobj, *args, **kwargs):
    """
    Convert from xyY to XYZ.
    """
    # avoid division by zero
    if cobj.xyy_y == 0.0:
        xyz_x = 0.0
        xyz_y = 0.0
        xyz_z = 0.0
    else:
        xyz_x = (cobj.xyy_x * cobj.xyy_Y) / cobj.xyy_y
        xyz_y = cobj.xyy_Y
        xyz_z = ((1.0 - cobj.xyy_x - cobj.xyy_y) * xyz_y) / cobj.xyy_y

    return XYZColor(
        xyz_x, xyz_y, xyz_z, illuminant=cobj.illuminant, observer=cobj.observer)


# noinspection PyPep8Naming,PyUnusedLocal
@color_conversion_function(XYZColor, xyYColor)
def XYZ_to_xyY(cobj, *args, **kwargs):
    """
    Convert from XYZ to xyY.
    """
    xyz_sum = cobj.xyz_x + cobj.xyz_y + cobj.xyz_z
    # avoid division by zero
    if xyz_sum == 0.0:
        xyy_x = 0.0
        xyy_y = 0.0
    else:
        xyy_x = cobj.xyz_x / xyz_sum
        xyy_y = cobj.xyz_y / xyz_sum
    xyy_Y = cobj.xyz_y

    return xyYColor(
        xyy_x, xyy_y, xyy_Y, observer=cobj.observer, illuminant=cobj.illuminant)


# noinspection PyPep8Naming,PyUnusedLocal
@color_conversion_function(XYZColor, LuvColor)
def XYZ_to_Luv(cobj, *args, **kwargs):
    """
    Convert from XYZ to Luv
    """
    temp_x = cobj.xyz_x
    temp_y = cobj.xyz_y
    temp_z = cobj.xyz_z
    denom = temp_x + (15.0 * temp_y) + (3.0 * temp_z)
    # avoid division by zero
    if denom == 0.0:
        luv_u = 0.0
        luv_v = 0.0
    else:
        luv_u = (4.0 * temp_x) / denom
        luv_v = (9.0 * temp_y) / denom

    illum = cobj.get_illuminant_xyz()
    temp_y = temp_y / illum["Y"]
    if temp_y > color_constants.CIE_E:
        temp_y = math.pow(temp_y, (1.0 / 3.0))
    else:
        temp_y = (7.787 * temp_y) + (16.0 / 116.0)

    ref_U = (4.0 * illum["X"]) / (illum["X"] + (15.0 * illum["Y"]) + (3.0 * illum["Z"]))
    ref_V = (9.0 * illum["Y"]) / (illum["X"] + (15.0 * illum["Y"]) + (3.0 * illum["Z"]))

    luv_l = (116.0 * temp_y) - 16.0
    luv_u = 13.0 * luv_l * (luv_u - ref_U)
    luv_v = 13.0 * luv_l * (luv_v - ref_V)

    return LuvColor(
        luv_l, luv_u, luv_v, observer=cobj.observer, illuminant=cobj.illuminant)


# noinspection PyPep8Naming,PyUnusedLocal
@color_conversion_function(XYZColor, LabColor)
def XYZ_to_Lab(cobj, *args, **kwargs):
    """
    Converts XYZ to Lab.
    """
    illum = cobj.get_illuminant_xyz()
    temp_x = cobj.xyz_x / illum["X"]
    temp_y = cobj.xyz_y / illum["Y"]
    temp_z = cobj.xyz_z / illum["Z"]

    if temp_x > color_constants.CIE_E:
        temp_x = math.pow(temp_x, (1.0 / 3.0))
    else:
        temp_x = (7.787 * temp_x) + (16.0 / 116.0)

    if temp_y > color_constants.CIE_E:
        temp_y = math.pow(temp_y, (1.0 / 3.0))
    else:
        temp_y = (7.787 * temp_y) + (16.0 / 116.0)

    if temp_z > color_constants.CIE_E:
        temp_z = math.pow(temp_z, (1.0 / 3.0))
    else:
        temp_z = (7.787 * temp_z) + (16.0 / 116.0)

    lab_l = (116.0 * temp_y) - 16.0
    lab_a = 500.0 * (temp_x - temp_y)
    lab_b = 200.0 * (temp_y - temp_z)
    return LabColor(
        lab_l, lab_a, lab_b, observer=cobj.observer, illuminant=cobj.illuminant)


# noinspection PyPep8Naming,PyUnusedLocal
@color_conversion_function(XYZColor, BaseRGBColor)
def XYZ_to_RGB(cobj, target_rgb, *args, **kwargs):
    """
    XYZ to RGB conversion.
    """
    temp_X = cobj.xyz_x
    temp_Y = cobj.xyz_y
    temp_Z = cobj.xyz_z

    logger.debug("  \- Target RGB space: %s", target_rgb)
    target_illum = target_rgb.native_illuminant
    logger.debug("  \- Target native illuminant: %s", target_illum)
    logger.debug("  \- XYZ color's illuminant: %s", cobj.illuminant)

    # If the XYZ values were taken with a different reference white than the
    # native reference white of the target RGB space, a transformation matrix
    # must be applied.
    if cobj.illuminant != target_illum:
        logger.debug("  \* Applying transformation from %s to %s ",
                     cobj.illuminant, target_illum)
        # Get the adjusted XYZ values, adapted for the target illuminant.
        temp_X, temp_Y, temp_Z = apply_chromatic_adaptation(
            temp_X, temp_Y, temp_Z,
            orig_illum=cobj.illuminant, targ_illum=target_illum)
        logger.debug("  \*   New values: %.3f, %.3f, %.3f",
                     temp_X, temp_Y, temp_Z)

    # Apply an RGB working space matrix to the XYZ values (matrix mul).
    rgb_r, rgb_g, rgb_b = apply_RGB_matrix(
        temp_X, temp_Y, temp_Z,
        rgb_type=target_rgb, convtype="xyz_to_rgb")

    # v
    linear_channels = dict(r=rgb_r, g=rgb_g, b=rgb_b)
    # V
    nonlinear_channels = {}
    if target_rgb == sRGBColor:
        for channel in ['r', 'g', 'b']:
            v = linear_channels[channel]
            if v <= 0.0031308:
                nonlinear_channels[channel] = v * 12.92
            else:
                nonlinear_channels[channel] = 1.055 * math.pow(v, 1 / 2.4) - 0.055
    else:
        # If it's not sRGB...
        for channel in ['r', 'g', 'b']:
            v = linear_channels[channel]
            nonlinear_channels[channel] = math.pow(v, 1 / target_rgb.rgb_gamma)

    return target_rgb(
        nonlinear_channels['r'], nonlinear_channels['g'], nonlinear_channels['b'])


# noinspection PyPep8Naming,PyUnusedLocal
@color_conversion_function(BaseRGBColor, XYZColor)
def RGB_to_XYZ(cobj, target_illuminant=None, *args, **kwargs):
    """
    RGB to XYZ conversion. Expects 0-255 RGB values.

    Based off of: http://www.brucelindbloom.com/index.html?Eqn_RGB_to_XYZ.html
    """
    # Will contain linearized RGB channels (removed the gamma func).
    linear_channels = {}

    if isinstance(cobj, sRGBColor):
        for channel in ['r', 'g', 'b']:
            V = getattr(cobj, 'rgb_' + channel)
            if V <= 0.04045:
                linear_channels[channel] = V / 12.92
            else:
                linear_channels[channel] = math.pow((V + 0.055) / 1.055, 2.4)
    else:
        # If it's not sRGB...
        gamma = cobj.rgb_gamma

        for channel in ['r', 'g', 'b']:
            V = getattr(cobj, 'rgb_' + channel)
            linear_channels[channel] = math.pow(V, gamma)

    # Apply an RGB working space matrix to the XYZ values (matrix mul).
    xyz_x, xyz_y, xyz_z = apply_RGB_matrix(
        linear_channels['r'], linear_channels['g'], linear_channels['b'],
        rgb_type=cobj, convtype="rgb_to_xyz")

    if target_illuminant is None:
        target_illuminant = cobj.native_illuminant

    # The illuminant of the original RGB object. This will always match
    # the RGB colorspace's native illuminant.
    illuminant = cobj.native_illuminant
    xyzcolor = XYZColor(xyz_x, xyz_y, xyz_z, illuminant=illuminant)
    # This will take care of any illuminant changes for us (if source
    # illuminant != target illuminant).
    xyzcolor.apply_adaptation(target_illuminant)

    return xyzcolor


# noinspection PyPep8Naming,PyUnusedLocal
def __RGB_to_Hue(var_R, var_G, var_B, var_min, var_max):
    """
    For RGB_to_HSL and RGB_to_HSV, the Hue (H) component is calculated in
    the same way.
    """
    if var_max == var_min:
        return 0.0
    elif var_max == var_R:
        return (60.0 * ((var_G - var_B) / (var_max - var_min)) + 360) % 360.0
    elif var_max == var_G:
        return 60.0 * ((var_B - var_R) / (var_max - var_min)) + 120
    elif var_max == var_B:
        return 60.0 * ((var_R - var_G) / (var_max - var_min)) + 240.0


# noinspection PyPep8Naming,PyUnusedLocal
@color_conversion_function(BaseRGBColor, HSVColor)
def RGB_to_HSV(cobj, *args, **kwargs):
    """
    Converts from RGB to HSV.

    H values are in degrees and are 0 to 360.
    S values are a percentage, 0.0 to 1.0.
    V values are a percentage, 0.0 to 1.0.
    """
    var_R = cobj.rgb_r
    var_G = cobj.rgb_g
    var_B = cobj.rgb_b

    var_max = max(var_R, var_G, var_B)
    var_min = min(var_R, var_G, var_B)

    var_H = __RGB_to_Hue(var_R, var_G, var_B, var_min, var_max)

    if var_max == 0:
        var_S = 0
    else:
        var_S = 1.0 - (var_min / var_max)

    var_V = var_max

    hsv_h = var_H
    hsv_s = var_S
    hsv_v = var_V

    return HSVColor(
        var_H, var_S, var_V)


# noinspection PyPep8Naming,PyUnusedLocal
@color_conversion_function(BaseRGBColor, HSLColor)
def RGB_to_HSL(cobj, *args, **kwargs):
    """
    Converts from RGB to HSL.

    H values are in degrees and are 0 to 360.
    S values are a percentage, 0.0 to 1.0.
    L values are a percentage, 0.0 to 1.0.
    """
    var_R = cobj.rgb_r
    var_G = cobj.rgb_g
    var_B = cobj.rgb_b

    var_max = max(var_R, var_G, var_B)
    var_min = min(var_R, var_G, var_B)

    var_H = __RGB_to_Hue(var_R, var_G, var_B, var_min, var_max)
    var_L = 0.5 * (var_max + var_min)

    if var_max == var_min:
        var_S = 0
    elif var_L <= 0.5:
        var_S = (var_max - var_min) / (2.0 * var_L)
    else:
        var_S = (var_max - var_min) / (2.0 - (2.0 * var_L))

    return HSLColor(
        var_H, var_S, var_L)


# noinspection PyPep8Naming,PyUnusedLocal
def __Calc_HSL_to_RGB_Components(var_q, var_p, C):
    """
    This is used in HSL_to_RGB conversions on R, G, and B.
    """
    if C < 0:
        C += 1.0
    if C > 1:
        C -= 1.0

    # Computing C of vector (Color R, Color G, Color B)
    if C < (1.0 / 6.0):
        return var_p + ((var_q - var_p) * 6.0 * C)
    elif (1.0 / 6.0) <= C < 0.5:
        return var_q
    elif 0.5 <= C < (2.0 / 3.0):
        return var_p + ((var_q - var_p) * 6.0 * ((2.0 / 3.0) - C))
    else:
        return var_p


# noinspection PyPep8Naming,PyUnusedLocal
@color_conversion_function(HSVColor, BaseRGBColor)
def HSV_to_RGB(cobj, target_rgb, *args, **kwargs):
    """
    HSV to RGB conversion.

    H values are in degrees and are 0 to 360.
    S values are a percentage, 0.0 to 1.0.
    V values are a percentage, 0.0 to 1.0.
    """
    H = cobj.hsv_h
    S = cobj.hsv_s
    V = cobj.hsv_v

    h_floored = int(math.floor(H))
    h_sub_i = int(h_floored / 60) % 6
    var_f = (H / 60.0) - (h_floored // 60)
    var_p = V * (1.0 - S)
    var_q = V * (1.0 - var_f * S)
    var_t = V * (1.0 - (1.0 - var_f) * S)

    if h_sub_i == 0:
        rgb_r = V
        rgb_g = var_t
        rgb_b = var_p
    elif h_sub_i == 1:
        rgb_r = var_q
        rgb_g = V
        rgb_b = var_p
    elif h_sub_i == 2:
        rgb_r = var_p
        rgb_g = V
        rgb_b = var_t
    elif h_sub_i == 3:
        rgb_r = var_p
        rgb_g = var_q
        rgb_b = V
    elif h_sub_i == 4:
        rgb_r = var_t
        rgb_g = var_p
        rgb_b = V
    elif h_sub_i == 5:
        rgb_r = V
        rgb_g = var_p
        rgb_b = var_q
    else:
        raise ValueError("Unable to convert HSL->RGB due to value error.")

    # In the event that they define an HSV color and want to convert it to
    # a particular RGB space, let them override it here.
    if target_rgb is not None:
        rgb_type = target_rgb
    else:
        rgb_type = cobj.rgb_type

    return target_rgb(rgb_r, rgb_g, rgb_b)


# noinspection PyPep8Naming,PyUnusedLocal
@color_conversion_function(HSLColor, BaseRGBColor)
def HSL_to_RGB(cobj, target_rgb, *args, **kwargs):
    """
    HSL to RGB conversion.
    """
    H = cobj.hsl_h
    S = cobj.hsl_s
    L = cobj.hsl_l

    if L < 0.5:
        var_q = L * (1.0 + S)
    else:
        var_q = L + S - (L * S)

    var_p = 2.0 * L - var_q

    # H normalized to range [0,1]
    h_sub_k = (H / 360.0)

    t_sub_R = h_sub_k + (1.0 / 3.0)
    t_sub_G = h_sub_k
    t_sub_B = h_sub_k - (1.0 / 3.0)

    rgb_r = __Calc_HSL_to_RGB_Components(var_q, var_p, t_sub_R)
    rgb_g = __Calc_HSL_to_RGB_Components(var_q, var_p, t_sub_G)
    rgb_b = __Calc_HSL_to_RGB_Components(var_q, var_p, t_sub_B)

    # In the event that they define an HSV color and want to convert it to
    # a particular RGB space, let them override it here.
    if target_rgb is not None:
        rgb_type = target_rgb
    else:
        rgb_type = cobj.rgb_type

    return target_rgb(rgb_r, rgb_g, rgb_b)


# noinspection PyPep8Naming,PyUnusedLocal
@color_conversion_function(BaseRGBColor, CMYColor)
def RGB_to_CMY(cobj, *args, **kwargs):
    """
    RGB to CMY conversion.

    NOTE: CMYK and CMY values range from 0.0 to 1.0
    """
    cmy_c = 1.0 - cobj.rgb_r
    cmy_m = 1.0 - cobj.rgb_g
    cmy_y = 1.0 - cobj.rgb_b

    return CMYColor(cmy_c, cmy_m, cmy_y)


# noinspection PyPep8Naming,PyUnusedLocal
@color_conversion_function(CMYColor, BaseRGBColor)
def CMY_to_RGB(cobj, target_rgb, *args, **kwargs):
    """
    Converts CMY to RGB via simple subtraction.

    NOTE: Returned values are in the range of 0-255.
    """
    rgb_r = 1.0 - cobj.cmy_c
    rgb_g = 1.0 - cobj.cmy_m
    rgb_b = 1.0 - cobj.cmy_y

    return target_rgb(rgb_r, rgb_g, rgb_b)


# noinspection PyPep8Naming,PyUnusedLocal
@color_conversion_function(CMYColor, CMYKColor)
def CMY_to_CMYK(cobj, *args, **kwargs):
    """
    Converts from CMY to CMYK.

    NOTE: CMYK and CMY values range from 0.0 to 1.0
    """
    var_k = 1.0
    if cobj.cmy_c < var_k:
        var_k = cobj.cmy_c
    if cobj.cmy_m < var_k:
        var_k = cobj.cmy_m
    if cobj.cmy_y < var_k:
        var_k = cobj.cmy_y

    if var_k == 1:
        cmyk_c = 0.0
        cmyk_m = 0.0
        cmyk_y = 0.0
    else:
        cmyk_c = (cobj.cmy_c - var_k) / (1.0 - var_k)
        cmyk_m = (cobj.cmy_m - var_k) / (1.0 - var_k)
        cmyk_y = (cobj.cmy_y - var_k) / (1.0 - var_k)
    cmyk_k = var_k

    return CMYKColor(cmyk_c, cmyk_m, cmyk_y, cmyk_k)


# noinspection PyPep8Naming,PyUnusedLocal
@color_conversion_function(CMYKColor, CMYColor)
def CMYK_to_CMY(cobj, *args, **kwargs):
    """
    Converts CMYK to CMY.

    NOTE: CMYK and CMY values range from 0.0 to 1.0
    """
    cmy_c = cobj.cmyk_c * (1.0 - cobj.cmyk_k) + cobj.cmyk_k
    cmy_m = cobj.cmyk_m * (1.0 - cobj.cmyk_k) + cobj.cmyk_k
    cmy_y = cobj.cmyk_y * (1.0 - cobj.cmyk_k) + cobj.cmyk_k

    return CMYColor(cmy_c, cmy_m, cmy_y)


# noinspection PyPep8Naming,PyUnusedLocal
@color_conversion_function(XYZColor, IPTColor)
def XYZ_to_IPT(cobj, *args, **kwargs):
    """
    Converts XYZ to IPT.

    NOTE: XYZ values need to be adapted to 2 degree D65

    Reference:
    Fairchild, M. D. (2013). Color appearance models, 3rd Ed. (pp. 271-272). John Wiley & Sons.
    """
    if cobj.illuminant != 'd65' or cobj.observer != '2':
        raise ValueError('XYZColor for XYZ->IPT conversion needs to be D65 adapted.')
    xyz_values = numpy.array(cobj.get_value_tuple())
    lms_values = numpy.dot(
        IPTColor.conversion_matrices['xyz_to_lms'],
        xyz_values)

    lms_prime = numpy.sign(lms_values) * numpy.abs(lms_values) ** 0.43

    ipt_values = numpy.dot(
        IPTColor.conversion_matrices['lms_to_ipt'],
        lms_prime)
    return IPTColor(*ipt_values)


# noinspection PyPep8Naming,PyUnusedLocal
@color_conversion_function(IPTColor, XYZColor)
def IPT_to_XYZ(cobj, *args, **kwargs):
    """
    Converts IPT to XYZ.
    """
    ipt_values = numpy.array(cobj.get_value_tuple())
    lms_values = numpy.dot(
        numpy.linalg.inv(IPTColor.conversion_matrices['lms_to_ipt']),
        ipt_values)

    lms_prime = numpy.sign(lms_values) * numpy.abs(lms_values) ** (1 / 0.43)

    xyz_values = numpy.dot(
        numpy.linalg.inv(IPTColor.conversion_matrices['xyz_to_lms']),
        lms_prime)
    return XYZColor(*xyz_values, observer='2', illuminant='d65')


# We use this as a template conversion dict for each RGB color space. They
# are all identical.
_RGB_CONVERSION_DICT_TEMPLATE = {
    "HSLColor": [RGB_to_HSL],
    "HSVColor": [RGB_to_HSV],
    "CMYColor": [RGB_to_CMY],
    "CMYKColor": [RGB_to_CMY, CMY_to_CMYK],
    "XYZColor": [RGB_to_XYZ],
    "xyYColor": [RGB_to_XYZ, XYZ_to_xyY],
    "LabColor": [RGB_to_XYZ, XYZ_to_Lab],
    "LCHabColor": [RGB_to_XYZ, XYZ_to_Lab, Lab_to_LCHab],
    "LCHuvColor": [RGB_to_XYZ, XYZ_to_Luv, Luv_to_LCHuv],
    "LuvColor": [RGB_to_XYZ, XYZ_to_Luv],
    "IPTColor": [RGB_to_XYZ, XYZ_to_IPT],

}


def convert_color(color, target_cs, through_rgb_type=sRGBColor,
                  target_illuminant=None, *args, **kwargs):
    """
    Converts the color to the designated color space.

    :param color: A Color instance to convert.
    :param target_cs: The Color class to convert to. Note that this is not
        an instance, but a class.
    :keyword BaseRGBColor through_rgb_type: If during your conversion between
        your original and target color spaces you have to pass through RGB,
        this determines which kind of RGB to use. For example, XYZ->HSL.
        You probably don't need to specify this unless you have a special
        usage case.
    :type target_illuminant: None or str
    :keyword target_illuminant: If during conversion from RGB to a reflective
        color space you want to explicitly end up with a certain illuminant,
        pass this here. Otherwise the RGB space's native illuminant
        will be used.
    :returns: An instance of the type passed in as ``target_cs``.
    :raises: :py:exc:`colormath.color_exceptions.UndefinedConversionError`
        if conversion between the two color spaces isn't possible.
    """
    if isinstance(target_cs, str):
        raise ValueError("target_cs parameter must be a Color object.")
    if not issubclass(target_cs, ColorBase):
        raise ValueError("target_cs parameter must be a Color object.")

    conversions = _conversion_manager.get_conversion_path(color.__class__, target_cs)

    logger.debug('Converting %s to %s', color, target_cs)
    logger.debug(' @ Conversion path: %s', conversions)

    # Start with original color in case we convert to the same color space.
    new_color = color

    if issubclass(target_cs, BaseRGBColor):
        # If the target_cs is an RGB color space of some sort, then we
        # have to set our through_rgb_type to make sure the conversion returns
        # the expected RGB colorspace (instead of defaulting to sRGBColor).
        through_rgb_type = target_cs

    # We have to be careful to use the same RGB color space that created
    # an object (if it was created by a conversion) in order to get correct
    # results. For example, XYZ->HSL via Adobe RGB should default to Adobe
    # RGB when taking that generated HSL object back to XYZ.
    # noinspection PyProtectedMember
    if through_rgb_type != sRGBColor:
        # User overrides take priority over everything.
        # noinspection PyProtectedMember
        target_rgb = through_rgb_type
    elif color._through_rgb_type:
        # Otherwise, a value on the color object is the next best thing,
        # when available.
        # noinspection PyProtectedMember
        target_rgb = color._through_rgb_type
    else:
        # We could collapse this into a single if statement above,
        # but I think this reads better.
        target_rgb = through_rgb_type

    # Iterate through the list of functions for the conversion path, storing
    # the results in a dictionary via update(). This way the user has access
    # to all of the variables involved in the conversion.
    for func in conversions:
        # Execute the function in this conversion step and store the resulting
        # Color object.
        logger.debug(' * Conversion: %s passed to %s()',
                     new_color.__class__.__name__, func)
        logger.debug(' |->  in %s', new_color)

        if func:
            # This can be None if you try to convert a color to the color
            # space that is already in. IE: XYZ->XYZ.
            new_color = func(
                new_color,
                target_rgb=target_rgb,
                target_illuminant=target_illuminant,
                *args, **kwargs)

        logger.debug(' |-< out %s', new_color)

    # If this conversion had something other than the default sRGB color space
    # requested,
    if through_rgb_type != sRGBColor:
        new_color._through_rgb_type = through_rgb_type

    return new_color
