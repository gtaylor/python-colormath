"""
This module contains classes to represent various color spaces.
"""

import logging
import math

import numpy as np

from colormath import color_conversions
from colormath import color_constants
from colormath import density
from colormath import color_diff, color_diff_matrix
from colormath.color_exceptions import InvalidConversion, InvalidObserver, \
    MissingValue, InvalidValue, InvalidDeltaEMode, InvalidIlluminant, \
    InvalidArgument

logger = logging.getLogger(__name__)


class ColorBase(object):
    """
    A base class holding some common methods and values.
    """

    # This is a table of conversions to/from this color space in the
    # sub-classed color class.
    CONVERSIONS = {}
    # Attribute names containing color data on the sub-class. For example,
    # the RGBColor would be ['rgb_r', 'rgb_g', 'rgb_b']
    VALUES = []

    def __prep_strings(self):
        """
        Makes sure all string variables are lowercase beforehand.
        """

        pass

    def convert_to(self, cs_to, *args, **kwargs):
        """
        Converts the color to the designated colorspace.
        """

        try:
            # Look up the conversion path for the specified color space.
            conversions = self.CONVERSIONS[cs_to.lower()]
        except KeyError:
            raise InvalidConversion(self.__class__.__name__, cs_to)

        # Make sure any string variables are lowercase.
        self.__prep_strings()
        # Make sure the object has all of its required values before even
        # attempting a conversion.
        self.has_required_values()

        logger.debug('Converting %s to %s', self, cs_to)
        logger.debug(' @ Conversion path: %s', conversions)

        cobj = self
        # Iterate through the list of functions for the conversion path, storing
        # the results in a dictionary via update(). This way the user has access
        # to all of the variables involved in the conversion.
        for func in conversions:
            # Execute the function in this conversion step and store the resulting
            # Color object.
            logger.debug(' * Conversion: %s passed to %s()',
                         cobj.__class__.__name__, func)
            logger.debug(' |->  in %s', cobj)

            if func:
                # This can be None if you try to convert a color to the color
                # space that is already in. IE: XYZ->XYZ.
                cobj = func(cobj, *args, **kwargs)

            logger.debug(' |-< out %s', cobj)
        return cobj

    def get_value_tuple(self):
        """
        Returns a tuple of the color's values (in order). For example,
        an LabColor object will return (lab_l, lab_a, lab_b), where each
        member of the tuple is the float value for said variable.
        """

        retval = tuple()
        for val in self.VALUES:
            retval += (getattr(self, val, None),)
        return retval

    def __str__(self):
        """
        String representation of the color.
        """

        retval = self.__class__.__name__ + ' ('
        for val in self.VALUES:
            value = getattr(self, val, None)
            if value is not None:
                retval += '%s:%.4f ' % (val, getattr(self, val))
        return retval.strip() + ')'

    def __repr__(self):
        """
        String representation of the object.
        """

        retval = self.__class__.__name__ + '('
        attributes = [(attr, getattr(self, attr)) for attr in self.VALUES]
        values = [x + "=" + repr(y) for x, y in attributes]
        retval += ','.join(values)
        return retval + ')'

    def has_required_values(self):
        """
        Checks various fields for None or invalid values.
        """

        for val in self.VALUES:
            value = getattr(self, val, None)
            if value is None:
                # A required value is missing.
                raise MissingValue(self, val)

            try:
                # If this fails, it's not a usable number.
                float(value)
            except ValueError:
                raise InvalidValue(self, val, value)
        return True

    def delta_e(self, other_color, mode='cie2000', *args, **kwargs):
        """
        Compares this color to another via Delta E.

        Valid modes:
         cie2000
         cie1994
         cie1976
         cmc
        """

        if not isinstance(other_color, ColorBase):
            raise InvalidArgument('delta_e_cie2000', 'other_color', other_color)

        # Convert the colors to Lab if they are not already.
        lab1 = self.convert_to('lab', *args, **kwargs)
        lab2 = other_color.convert_to('lab', *args, **kwargs)

        mode = mode.lower()
        if mode == 'cie2000':
            return color_diff.delta_e_cie2000(lab1, lab2)
        elif mode == 'cie1994':
            return color_diff.delta_e_cie1994(lab1, lab2, **kwargs)
        elif mode == 'cie1976':
            return color_diff.delta_e_cie1976(lab1, lab2)
        elif mode == 'cmc':
            return color_diff.delta_e_cmc(lab1, lab2, **kwargs)
        else:
            raise InvalidDeltaEMode(mode)


class ColorBaseWithIlluminant(ColorBase):

    # noinspection PyAttributeOutsideInit
    def __prep_strings(self):
        """
        Makes sure all string variables are lowercase beforehand.
        """

        self.illuminant = self.illuminant.lower()
        self.observer = str(self.observer)

    # noinspection PyAttributeOutsideInit
    def set_illuminant(self, illuminant):
        self.illuminant = illuminant.lower()

    # noinspection PyAttributeOutsideInit
    def set_observer(self, observer):
        if observer not in ['2', '10']:
            raise InvalidObserver(self)
        self.observer = observer

    def has_required_values(self):
        """
        Checks various fields for None or invalid values.
        """

        if self.observer not in ['2', '10']:
            raise InvalidObserver(self)

        super(ColorBaseWithIlluminant, self).has_required_values()

    def get_illuminant_xyz(self, observer=None, illuminant=None):
        """
        :param str observer: Get the XYZ values for another observer angle. Must
            be either '2' or '10'.
        :param str illuminant: Get the XYZ values for another illuminant.
        :returns: the color's illuminant's XYZ values.
        """

        try:
            if observer is None:
                observer = self.observer

            illums_observer = color_constants.ILLUMINANTS[observer]
        except KeyError:
            raise InvalidObserver(self)

        try:
            if illuminant is None:
                illuminant = self.illuminant

            illum_xyz = illums_observer[illuminant]
        except AttributeError:
            raise InvalidIlluminant(self)
        except KeyError:
            raise InvalidIlluminant(self)

        return {'X': illum_xyz[0], 'Y': illum_xyz[1], 'Z': illum_xyz[2]}


class SpectralColor(ColorBaseWithIlluminant):
    """
    Represents a color that may have operations done to it. You need not use
    this object with the library as long as you use all of the instance
    variables here.
    """

    CONVERSIONS = {
        "spectral": [None],
        "xyz": [color_conversions.Spectral_to_XYZ],
        "xyy": [color_conversions.Spectral_to_XYZ, color_conversions.XYZ_to_xyY],
        "lab": [color_conversions.Spectral_to_XYZ, color_conversions.XYZ_to_Lab],
        "lch": [color_conversions.Spectral_to_XYZ, color_conversions.XYZ_to_Lab,
                color_conversions.Lab_to_LCHab],
        "luv": [color_conversions.Spectral_to_XYZ, color_conversions.XYZ_to_Luv],
        "rgb": [color_conversions.Spectral_to_XYZ, color_conversions.XYZ_to_RGB],
        "hsl": [color_conversions.Spectral_to_XYZ, color_conversions.XYZ_to_RGB,
                color_conversions.RGB_to_HSL],
        "hsv": [color_conversions.Spectral_to_XYZ, color_conversions.XYZ_to_RGB,
                color_conversions.RGB_to_HSV],
        "cmy": [color_conversions.Spectral_to_XYZ, color_conversions.XYZ_to_RGB,
                color_conversions.RGB_to_CMY],
       "cmyk": [color_conversions.Spectral_to_XYZ, color_conversions.XYZ_to_RGB,
                color_conversions.RGB_to_CMY, color_conversions.CMY_to_CMYK],
    }
    VALUES = [
        'spec_340nm', 'spec_350nm', 'spec_360nm', 'spec_370nm',
        'spec_380nm', 'spec_390nm', 'spec_400nm', 'spec_410nm',
        'spec_420nm', 'spec_430nm', 'spec_440nm', 'spec_450nm',
        'spec_460nm', 'spec_470nm', 'spec_480nm', 'spec_490nm',
        'spec_500nm', 'spec_510nm', 'spec_520nm', 'spec_530nm',
        'spec_540nm', 'spec_550nm', 'spec_560nm', 'spec_570nm',
        'spec_580nm', 'spec_590nm', 'spec_600nm', 'spec_610nm',
        'spec_620nm', 'spec_630nm', 'spec_640nm', 'spec_650nm',
        'spec_660nm', 'spec_670nm', 'spec_680nm', 'spec_690nm',
        'spec_700nm', 'spec_710nm', 'spec_720nm', 'spec_730nm',
        'spec_740nm', 'spec_750nm', 'spec_760nm', 'spec_770nm',
        'spec_780nm', 'spec_790nm', 'spec_800nm', 'spec_810nm',
        'spec_820nm', 'spec_830nm'
    ]

    def __init__(self,
        spec_340nm=0.0, spec_350nm=0.0, spec_360nm=0.0, spec_370nm=0.0,
        spec_380nm=0.0, spec_390nm=0.0, spec_400nm=0.0, spec_410nm=0.0,
        spec_420nm=0.0, spec_430nm=0.0, spec_440nm=0.0, spec_450nm=0.0,
        spec_460nm=0.0, spec_470nm=0.0, spec_480nm=0.0, spec_490nm=0.0,
        spec_500nm=0.0, spec_510nm=0.0, spec_520nm=0.0, spec_530nm=0.0,
        spec_540nm=0.0, spec_550nm=0.0, spec_560nm=0.0, spec_570nm=0.0,
        spec_580nm=0.0, spec_590nm=0.0, spec_600nm=0.0, spec_610nm=0.0,
        spec_620nm=0.0, spec_630nm=0.0, spec_640nm=0.0, spec_650nm=0.0,
        spec_660nm=0.0, spec_670nm=0.0, spec_680nm=0.0, spec_690nm=0.0,
        spec_700nm=0.0, spec_710nm=0.0, spec_720nm=0.0, spec_730nm=0.0,
        spec_740nm=0.0, spec_750nm=0.0, spec_760nm=0.0, spec_770nm=0.0,
        spec_780nm=0.0, spec_790nm=0.0, spec_800nm=0.0, spec_810nm=0.0,
        spec_820nm=0.0, spec_830nm=0.0, illuminant='d50', observer='2'):

        super(SpectralColor, self).__init__()
        # Spectral fields
        self.spec_340nm = float(spec_340nm)
        self.spec_350nm = float(spec_350nm)
        self.spec_360nm = float(spec_360nm)
        self.spec_370nm = float(spec_370nm)
        # begin Blue wavelengths
        self.spec_380nm = float(spec_380nm)
        self.spec_390nm = float(spec_390nm)
        self.spec_400nm = float(spec_400nm)
        self.spec_410nm = float(spec_410nm)
        self.spec_420nm = float(spec_420nm)
        self.spec_430nm = float(spec_430nm)
        self.spec_440nm = float(spec_440nm)
        self.spec_450nm = float(spec_450nm)
        self.spec_460nm = float(spec_460nm)
        self.spec_470nm = float(spec_470nm)
        self.spec_480nm = float(spec_480nm)
        self.spec_490nm = float(spec_490nm)
        # end Blue wavelengths
        # start Green wavelengths
        self.spec_500nm = float(spec_500nm)
        self.spec_510nm = float(spec_510nm)
        self.spec_520nm = float(spec_520nm)
        self.spec_530nm = float(spec_530nm)
        self.spec_540nm = float(spec_540nm)
        self.spec_550nm = float(spec_550nm)
        self.spec_560nm = float(spec_560nm)
        self.spec_570nm = float(spec_570nm)
        self.spec_580nm = float(spec_580nm)
        self.spec_590nm = float(spec_590nm)
        self.spec_600nm = float(spec_600nm)
        self.spec_610nm = float(spec_610nm)
        # end Green wavelengths
        # start Red wavelengths
        self.spec_620nm = float(spec_620nm)
        self.spec_630nm = float(spec_630nm)
        self.spec_640nm = float(spec_640nm)
        self.spec_650nm = float(spec_650nm)
        self.spec_660nm = float(spec_660nm)
        self.spec_670nm = float(spec_670nm)
        self.spec_680nm = float(spec_680nm)
        self.spec_690nm = float(spec_690nm)
        self.spec_700nm = float(spec_700nm)
        self.spec_710nm = float(spec_710nm)
        self.spec_720nm = float(spec_720nm)
        # end Red wavelengths
        self.spec_730nm = float(spec_730nm)
        self.spec_740nm = float(spec_740nm)
        self.spec_750nm = float(spec_750nm)
        self.spec_760nm = float(spec_760nm)
        self.spec_770nm = float(spec_770nm)
        self.spec_780nm = float(spec_780nm)
        self.spec_790nm = float(spec_790nm)
        self.spec_800nm = float(spec_800nm)
        self.spec_810nm = float(spec_810nm)
        self.spec_820nm = float(spec_820nm)
        self.spec_830nm = float(spec_830nm)

        self.set_illuminant(illuminant)
        self.set_observer(observer)

    def get_numpy_array(self):
        """
        Dump this color into NumPy array.
        """

        # This holds the obect's spectral data, and will be passed to
        # numpy.array() to create a numpy array (matrix) for the matrix math
        # that will be done during the conversion to XYZ.
        values = []

        # Use the required value list to build this dynamically. Default to
        # 0.0, since that ultimately won't affect the outcome due to the math
        # involved.
        for val in self.VALUES:
            values.append(getattr(self, val, 0.0))

        # Create and the actual numpy array/matrix from the spectral list.
        color_array = np.array([values])
        return color_array

    def calc_density(self, density_standard=None):
        """
        Calculates the density of the SpectralColor. By default, Status T
        density is used, and the correct density distribution (Red, Green,
        or Blue) is chosen by comparing the Red, Green, and Blue components of
        the spectral sample (the values being red in via "filters").
        """

        if density_standard is not None:
            return density.ansi_density(self, density_standard)
        else:
            return density.auto_density(self)


class LabColor(ColorBaseWithIlluminant):
    """
    Represents an Lab color.
    """

    CONVERSIONS = {
        "lab": [None],
        "xyz": [color_conversions.Lab_to_XYZ],
        "xyy": [color_conversions.Lab_to_XYZ, color_conversions.XYZ_to_xyY],
      "lchab": [color_conversions.Lab_to_LCHab],
      "lchuv": [color_conversions.Lab_to_XYZ, color_conversions.XYZ_to_Luv,
                color_conversions.Luv_to_LCHuv],
        "luv": [color_conversions.Lab_to_XYZ, color_conversions.XYZ_to_Luv],
        "rgb": [color_conversions.Lab_to_XYZ, color_conversions.XYZ_to_RGB],
        "hsl": [color_conversions.Lab_to_XYZ, color_conversions.XYZ_to_RGB,
                color_conversions.RGB_to_HSL],
        "hsv": [color_conversions.Lab_to_XYZ, color_conversions.XYZ_to_RGB,
                color_conversions.RGB_to_HSV],
        "cmy": [color_conversions.Lab_to_XYZ, color_conversions.XYZ_to_RGB,
                color_conversions.RGB_to_CMY],
       "cmyk": [color_conversions.Lab_to_XYZ, color_conversions.XYZ_to_RGB,
                color_conversions.RGB_to_CMY, color_conversions.CMY_to_CMYK],
    }
    VALUES = ['lab_l', 'lab_a', 'lab_b']

    def __init__(self, lab_l, lab_a, lab_b, illuminant='d50', observer='2'):
        super(LabColor, self).__init__()
        self.lab_l = float(lab_l)
        self.lab_a = float(lab_a)
        self.lab_b = float(lab_b)
        self.set_illuminant(illuminant)
        self.set_observer(observer)

    # noinspection PyUnusedLocal
    def delta_e_matrix(self, lab_color_matrix, mode='cie2000', *args, **kwargs):
        """
        Compares this object with all colors in lab_color_matrix via Delta E.
        The matrix must be of shape (n,3) and must be composed of floats.
        Returns a distance vector of shape (n,).

        Valid modes:
         cie2000
         cie1976
         cie1994
         cmc
        """

        lab_color_vector = np.array([self.lab_l, self.lab_a, self.lab_b])

        mode = mode.lower()

        if mode == 'cie2000':
            return color_diff_matrix.delta_e_cie2000(
                lab_color_vector, lab_color_matrix)
        elif mode == 'cie1994':
            return color_diff_matrix.delta_e_cie1994(
                lab_color_vector, lab_color_matrix, **kwargs)
        elif mode == 'cie1976':
            return color_diff_matrix.delta_e_cie1976(
                lab_color_vector, lab_color_matrix)
        elif mode == 'cmc':
            return color_diff_matrix.delta_e_cmc(
                lab_color_vector, lab_color_matrix, **kwargs)
        else:
            raise InvalidDeltaEMode(mode)


class LCHabColor(ColorBaseWithIlluminant):
    """
    Represents an LCHab color.
    """

    CONVERSIONS = {
      "lchab": [None],
        "xyz": [color_conversions.LCHab_to_Lab, color_conversions.Lab_to_XYZ],
        "xyy": [color_conversions.LCHab_to_Lab, color_conversions.Lab_to_XYZ,
                color_conversions.XYZ_to_xyY],
        "lab": [color_conversions.LCHab_to_Lab],
      "lchuv": [color_conversions.LCHab_to_Lab, color_conversions.Lab_to_XYZ,
                color_conversions.XYZ_to_Luv, color_conversions.Luv_to_LCHuv],
        "luv": [color_conversions.LCHab_to_Lab, color_conversions.Lab_to_XYZ,
                color_conversions.XYZ_to_Luv],
        "rgb": [color_conversions.LCHab_to_Lab, color_conversions.Lab_to_XYZ,
                color_conversions.XYZ_to_RGB],
        "hsl": [color_conversions.LCHab_to_Lab, color_conversions.Lab_to_XYZ,
                color_conversions.XYZ_to_RGB, color_conversions.RGB_to_HSL],
        "hsv": [color_conversions.LCHab_to_Lab, color_conversions.Lab_to_XYZ,
                color_conversions.XYZ_to_RGB, color_conversions.RGB_to_HSV],
        "cmy": [color_conversions.LCHab_to_Lab, color_conversions.Lab_to_XYZ,
                color_conversions.XYZ_to_RGB, color_conversions.RGB_to_CMY],
       "cmyk": [color_conversions.LCHab_to_Lab, color_conversions.Lab_to_XYZ,
                color_conversions.XYZ_to_RGB, color_conversions.RGB_to_CMY,
                color_conversions.CMY_to_CMYK],
    }
    VALUES = ['lch_l', 'lch_c', 'lch_h']

    def __init__(self, lch_l, lch_c, lch_h, illuminant='d50', observer='2'):
        super(LCHabColor, self).__init__()
        self.lch_l = float(lch_l)
        self.lch_c = float(lch_c)
        self.lch_h = float(lch_h)
        self.set_illuminant(illuminant)
        self.set_observer(observer)


class LCHuvColor(ColorBaseWithIlluminant):
    """
    Represents an LCHuv color.
    """

    CONVERSIONS = {
      "lchuv": [None],
        "xyz": [color_conversions.LCHuv_to_Luv, color_conversions.Luv_to_XYZ],
        "xyy": [color_conversions.LCHuv_to_Luv, color_conversions.Luv_to_XYZ,
                color_conversions.XYZ_to_xyY],
        "lab": [color_conversions.LCHuv_to_Luv, color_conversions.Luv_to_XYZ,
                color_conversions.XYZ_to_Lab],
        "luv": [color_conversions.LCHuv_to_Luv],
      "lchab": [color_conversions.LCHuv_to_Luv, color_conversions.Luv_to_XYZ,
                color_conversions.XYZ_to_Lab, color_conversions.Lab_to_LCHab],
        "rgb": [color_conversions.LCHuv_to_Luv, color_conversions.Luv_to_XYZ,
                color_conversions.XYZ_to_RGB],
        "hsl": [color_conversions.LCHuv_to_Luv, color_conversions.Luv_to_XYZ,
                color_conversions.XYZ_to_RGB, color_conversions.RGB_to_HSL],
        "hsv": [color_conversions.LCHuv_to_Luv, color_conversions.Luv_to_XYZ,
                color_conversions.XYZ_to_RGB, color_conversions.RGB_to_HSV],
        "cmy": [color_conversions.LCHuv_to_Luv, color_conversions.Luv_to_XYZ,
                color_conversions.XYZ_to_RGB, color_conversions.RGB_to_CMY],
       "cmyk": [color_conversions.LCHuv_to_Luv, color_conversions.Luv_to_XYZ,
                color_conversions.XYZ_to_RGB, color_conversions.RGB_to_CMY,
                color_conversions.CMY_to_CMYK],
    }
    VALUES = ['lch_l', 'lch_c', 'lch_h']

    def __init__(self, lch_l, lch_c, lch_h, illuminant='d50', observer='2'):
        super(LCHuvColor, self).__init__()
        self.lch_l = float(lch_l)
        self.lch_c = float(lch_c)
        self.lch_h = float(lch_h)
        self.set_illuminant(illuminant)
        self.set_observer(observer)


class LuvColor(ColorBaseWithIlluminant):
    """
    Represents an Luv color.
    """

    CONVERSIONS = {
        "luv": [None],
        "xyz": [color_conversions.Luv_to_XYZ],
        "xyy": [color_conversions.Luv_to_XYZ, color_conversions.XYZ_to_xyY],
        "lab": [color_conversions.Luv_to_XYZ, color_conversions.XYZ_to_Lab],
      "lchab": [color_conversions.Luv_to_XYZ, color_conversions.XYZ_to_Lab,
                color_conversions.Lab_to_LCHab],
      "lchuv": [color_conversions.Luv_to_LCHuv],
        "rgb": [color_conversions.Luv_to_XYZ, color_conversions.XYZ_to_RGB],
        "hsl": [color_conversions.Luv_to_XYZ, color_conversions.XYZ_to_RGB,
                color_conversions.RGB_to_HSL],
        "hsv": [color_conversions.Luv_to_XYZ, color_conversions.XYZ_to_RGB,
                color_conversions.RGB_to_HSV],
        "cmy": [color_conversions.Luv_to_XYZ, color_conversions.XYZ_to_RGB,
                color_conversions.RGB_to_CMY],
       "cmyk": [color_conversions.Luv_to_XYZ, color_conversions.XYZ_to_RGB,
                color_conversions.RGB_to_CMY, color_conversions.CMY_to_CMYK],
    }
    VALUES = ['luv_l', 'luv_u', 'luv_v']

    def __init__(self, luv_l, luv_u, luv_v, illuminant='d50', observer='2'):
        super(LuvColor, self).__init__()
        self.luv_l = float(luv_l)
        self.luv_u = float(luv_u)
        self.luv_v = float(luv_v)
        self.set_illuminant(illuminant)
        self.set_observer(observer)


class XYZColor(ColorBaseWithIlluminant):
    """
    Represents an XYZ color.
    """

    CONVERSIONS = {
        "xyz": [None],
        "xyy": [color_conversions.XYZ_to_xyY],
        "lab": [color_conversions.XYZ_to_Lab],
      "lchab": [color_conversions.XYZ_to_Lab, color_conversions.Lab_to_LCHab],
      "lchuv": [color_conversions.XYZ_to_Lab, color_conversions.Luv_to_LCHuv],
        "luv": [color_conversions.XYZ_to_Luv],
        "rgb": [color_conversions.XYZ_to_RGB],
        "hsl": [color_conversions.XYZ_to_RGB, color_conversions.RGB_to_HSL],
        "hsv": [color_conversions.XYZ_to_RGB, color_conversions.RGB_to_HSV],
        "cmy": [color_conversions.XYZ_to_RGB, color_conversions.RGB_to_CMY],
       "cmyk": [color_conversions.XYZ_to_RGB, color_conversions.RGB_to_CMY,
                color_conversions.CMY_to_CMYK],
    }
    VALUES = ['xyz_x', 'xyz_y', 'xyz_z']

    def __init__(self, xyz_x, xyz_y, xyz_z, illuminant='d50', observer='2'):
        super(XYZColor, self).__init__()
        self.xyz_x = float(xyz_x)
        self.xyz_y = float(xyz_y)
        self.xyz_z = float(xyz_z)
        self.set_illuminant(illuminant)
        self.set_observer(observer)

    def apply_adaptation(self, target_illuminant, adaptation='bradford'):
        """
        This applies an adaptation matrix to change the XYZ color's illuminant.
        You'll most likely only need this during RGB conversions.
        """

        # The illuminant of the original RGB object.
        source_illuminant = self.illuminant

        logger.debug("  \- Original illuminant: %s", self.illuminant)
        logger.debug("  \- Target illuminant: %s", target_illuminant)

        # If the XYZ values were taken with a different reference white than the
        # native reference white of the target RGB space, a transformation matrix
        # must be applied.
        if source_illuminant != target_illuminant:
            logger.debug("  \* Applying transformation from %s to %s ",
                         source_illuminant, target_illuminant)
            # Get the adjusted XYZ values, adapted for the target illuminant.
            self.xyz_x, self.xyz_y, self.xyz_z \
                = color_conversions.apply_XYZ_transformation(
                    self.xyz_x,
                    self.xyz_y,
                    self.xyz_z,
                    orig_illum=source_illuminant,
                    targ_illum=target_illuminant)
            # noinspection PyAttributeOutsideInit
            self.illuminant = target_illuminant.lower()


# noinspection PyPep8Naming
class xyYColor(ColorBaseWithIlluminant):
    """
    Represents an xYy color.
    """

    CONVERSIONS = {
        "xyy": [None],
        "xyz": [color_conversions.xyY_to_XYZ],
        "lab": [color_conversions.xyY_to_XYZ, color_conversions.XYZ_to_Lab],
      "lchab": [color_conversions.xyY_to_XYZ, color_conversions.XYZ_to_Lab,
                color_conversions.Lab_to_LCHab],
      "lchuv": [color_conversions.xyY_to_XYZ, color_conversions.XYZ_to_Luv,
                color_conversions.Luv_to_LCHuv],
        "luv": [color_conversions.xyY_to_XYZ, color_conversions.XYZ_to_Luv],
        "rgb": [color_conversions.xyY_to_XYZ, color_conversions.XYZ_to_RGB],
        "hsl": [color_conversions.xyY_to_XYZ, color_conversions.XYZ_to_RGB,
                color_conversions.RGB_to_HSL],
        "hsv": [color_conversions.xyY_to_XYZ, color_conversions.XYZ_to_RGB,
                color_conversions.RGB_to_HSV],
        "cmy": [color_conversions.xyY_to_XYZ, color_conversions.XYZ_to_RGB,
                color_conversions.RGB_to_CMY],
       "cmyk": [color_conversions.xyY_to_XYZ, color_conversions.XYZ_to_RGB,
                color_conversions.RGB_to_CMY, color_conversions.CMY_to_CMYK],
    }
    VALUES = ['xyy_x', 'xyy_y', 'xyy_Y']

    def __init__(self, xyy_x, xyy_y, xyy_Y, illuminant='d50', observer='2'):
        super(xyYColor, self).__init__()
        self.xyy_x = float(xyy_x)
        self.xyy_y = float(xyy_y)
        self.xyy_Y = float(xyy_Y)
        self.set_illuminant(illuminant)
        self.set_observer(observer)


class RGBColor(ColorBase):
    """
    Represents an RGB color.
    """

    CONVERSIONS = {
        "rgb": [None],
        "hsl": [color_conversions.RGB_to_HSL],
        "hsv": [color_conversions.RGB_to_HSV],
        "cmy": [color_conversions.RGB_to_CMY],
       "cmyk": [color_conversions.RGB_to_CMY, color_conversions.CMY_to_CMYK],
        "xyz": [color_conversions.RGB_to_XYZ],
        "xyy": [color_conversions.RGB_to_XYZ, color_conversions.XYZ_to_xyY],
        "lab": [color_conversions.RGB_to_XYZ, color_conversions.XYZ_to_Lab],
      "lchab": [color_conversions.RGB_to_XYZ, color_conversions.XYZ_to_Lab,
                color_conversions.Lab_to_LCHab],
      "lchuv": [color_conversions.RGB_to_XYZ, color_conversions.XYZ_to_Luv,
                color_conversions.Luv_to_LCHuv],
        "luv": [color_conversions.RGB_to_XYZ, color_conversions.XYZ_to_Luv],
    }
    VALUES = ['rgb_r', 'rgb_g', 'rgb_b']
    OTHER_VALUES = ['rgb_type']

    def __init__(self, rgb_r, rgb_g, rgb_b, rgb_type='srgb', is_upscaled=False):
        super(RGBColor, self).__init__()
        if is_upscaled:
            self.rgb_r = rgb_r / 255.0
            self.rgb_g = rgb_g / 255.0
            self.rgb_b = rgb_b / 255.0
        else:
            self.rgb_r = float(rgb_r)
            self.rgb_g = float(rgb_g)
            self.rgb_b = float(rgb_b)
        self.rgb_type = rgb_type.lower()

    def __str__(self):
        parent_str = super(RGBColor, self).__str__()
        return '%s [%s]' % (parent_str, self.rgb_type)

    def get_rgb_upscaled(self):
        """
        Scales an RGB color object from decimal 0.0-1.0 to int 0-255.
        """

        # Scale up to 0-255 values.
        rgb_r = int(math.floor(0.5 + self.rgb_r * 255))
        rgb_g = int(math.floor(0.5 + self.rgb_g * 255))
        rgb_b = int(math.floor(0.5 + self.rgb_b * 255))

        return rgb_r, rgb_g, rgb_b

    def get_rgb_hex(self):
        """
        Converts the RGB value to a hex value in the form of: #RRGGBB
        """

        rgb_r, rgb_g, rgb_b = self.get_rgb_upscaled()
        return '#%02x%02x%02x' % (rgb_r, rgb_g, rgb_b)

    @classmethod
    def new_from_rgb_hex(cls, hex_str):
        """
        Converts an RGB hex string like #RRGGBB and assigns the values to
        this RGBColor object.
        """

        colorstring = hex_str.strip()
        if colorstring[0] == '#':
            colorstring = colorstring[1:]
        if len(colorstring) != 6:
            raise ValueError("input #%s is not in #RRGGBB format" % colorstring)
        r, g, b = colorstring[:2], colorstring[2:4], colorstring[4:]
        r, g, b = [int(n, 16) / 255.0 for n in (r, g, b)]
        return cls(r, g, b)


class HSLColor(ColorBase):
    """
    Represents an HSL color.
    """

    CONVERSIONS = {
        "hsl": [None],
        "hsv": [color_conversions.HSL_to_RGB, color_conversions.RGB_to_HSV],
        "rgb": [color_conversions.HSL_to_RGB],
        "cmy": [color_conversions.HSL_to_RGB, color_conversions.RGB_to_CMY],
       "cmyk": [color_conversions.HSL_to_RGB, color_conversions.RGB_to_CMY,
                color_conversions.CMY_to_CMYK],
        "xyz": [color_conversions.HSL_to_RGB, color_conversions.RGB_to_XYZ],
        "xyy": [color_conversions.HSL_to_RGB, color_conversions.RGB_to_XYZ,
                color_conversions.XYZ_to_xyY],
        "lab": [color_conversions.HSL_to_RGB, color_conversions.RGB_to_XYZ,
                color_conversions.XYZ_to_Lab],
      "lchab": [color_conversions.HSL_to_RGB, color_conversions.RGB_to_XYZ,
                color_conversions.XYZ_to_Lab, color_conversions.Lab_to_LCHab],
      "lchuv": [color_conversions.HSL_to_RGB, color_conversions.RGB_to_XYZ,
                color_conversions.XYZ_to_Luv, color_conversions.Luv_to_LCHuv],
        "luv": [color_conversions.HSL_to_RGB, color_conversions.RGB_to_XYZ,
                color_conversions.XYZ_to_RGB],
    }
    VALUES = ['hsl_h', 'hsl_s', 'hsl_l']
    OTHER_VALUES = ['rgb_type']

    def __init__(self, hsl_h, hsl_s, hsl_l, rgb_type='srgb'):
        super(HSLColor, self).__init__()
        self.hsl_h = float(hsl_h)
        self.hsl_s = float(hsl_s)
        self.hsl_l = float(hsl_l)
        self.rgb_type = rgb_type.lower()


class HSVColor(ColorBase):
    """
    Represents an HSV color.
    """

    CONVERSIONS = {
        "hsv": [None],
        "hsl": [color_conversions.HSV_to_RGB, color_conversions.RGB_to_HSL],
        "rgb": [color_conversions.HSV_to_RGB],
        "cmy": [color_conversions.HSV_to_RGB, color_conversions.RGB_to_CMY],
       "cmyk": [color_conversions.HSV_to_RGB, color_conversions.RGB_to_CMY,
                color_conversions.CMY_to_CMYK],
        "xyz": [color_conversions.HSV_to_RGB, color_conversions.RGB_to_XYZ],
        "xyy": [color_conversions.HSV_to_RGB, color_conversions.RGB_to_XYZ,
                color_conversions.XYZ_to_xyY],
        "lab": [color_conversions.HSV_to_RGB, color_conversions.RGB_to_XYZ,
                color_conversions.XYZ_to_Lab],
      "lchab": [color_conversions.HSV_to_RGB, color_conversions.RGB_to_XYZ,
                color_conversions.XYZ_to_Lab, color_conversions.Lab_to_LCHab],
      "lchuv": [color_conversions.HSV_to_RGB, color_conversions.RGB_to_XYZ,
                color_conversions.XYZ_to_Luv, color_conversions.Luv_to_LCHuv],
        "luv": [color_conversions.HSV_to_RGB, color_conversions.RGB_to_XYZ,
                color_conversions.XYZ_to_RGB],
    }
    VALUES = ['hsv_h', 'hsv_s', 'hsv_v']
    OTHER_VALUES = ['rgb_type']

    def __init__(self, hsv_h, hsv_s, hsv_v, rgb_type='srgb'):
        super(HSVColor, self).__init__()
        self.hsv_h = float(hsv_h)
        self.hsv_s = float(hsv_s)
        self.hsv_v = float(hsv_v)
        self.rgb_type = rgb_type.lower()


class CMYColor(ColorBase):
    """
    Represents a CMY color.
    """

    CONVERSIONS = {
        "cmy": [None],
       "cmyk": [color_conversions.CMY_to_CMYK],
        "hsl": [color_conversions.CMY_to_RGB, color_conversions.RGB_to_HSL],
        "hsv": [color_conversions.CMY_to_RGB, color_conversions.RGB_to_HSV],
        "rgb": [color_conversions.CMY_to_RGB],
        "xyz": [color_conversions.CMY_to_RGB, color_conversions.RGB_to_XYZ],
        "xyy": [color_conversions.CMY_to_RGB, color_conversions.RGB_to_XYZ,
                color_conversions.XYZ_to_xyY],
        "lab": [color_conversions.CMY_to_RGB, color_conversions.RGB_to_XYZ,
                color_conversions.XYZ_to_Lab],
      "lchab": [color_conversions.CMY_to_RGB, color_conversions.RGB_to_XYZ,
                color_conversions.XYZ_to_Lab,
                color_conversions.Lab_to_LCHab],
      "lchuv": [color_conversions.CMY_to_RGB, color_conversions.RGB_to_XYZ,
                color_conversions.XYZ_to_Luv, color_conversions.Luv_to_LCHuv],
        "luv": [color_conversions.CMY_to_RGB, color_conversions.RGB_to_XYZ,
                color_conversions.XYZ_to_RGB],
    }
    VALUES = ['cmy_c', 'cmy_m', 'cmy_y']

    def __init__(self, cmy_c, cmy_m, cmy_y):
        super(CMYColor, self).__init__()
        self.cmy_c = float(cmy_c)
        self.cmy_m = float(cmy_m)
        self.cmy_y = float(cmy_y)


class CMYKColor(ColorBase):
    """
    Represents a CMYK color.
    """

    CONVERSIONS = {
       "cmyk": [None],
        "cmy": [color_conversions.CMYK_to_CMY],
        "hsl": [color_conversions.CMYK_to_CMY, color_conversions.CMY_to_RGB,
                color_conversions.RGB_to_HSL],
        "hsv": [color_conversions.CMYK_to_CMY, color_conversions.CMY_to_RGB,
                color_conversions.RGB_to_HSV],
        "rgb": [color_conversions.CMYK_to_CMY, color_conversions.CMY_to_RGB],
        "xyz": [color_conversions.CMYK_to_CMY, color_conversions.CMY_to_RGB,
                color_conversions.RGB_to_XYZ],
        "xyy": [color_conversions.CMYK_to_CMY, color_conversions.CMY_to_RGB,
                color_conversions.RGB_to_XYZ, color_conversions.XYZ_to_xyY],
        "lab": [color_conversions.CMYK_to_CMY, color_conversions.CMY_to_RGB,
                color_conversions.RGB_to_XYZ, color_conversions.XYZ_to_Lab],
      "lchab": [color_conversions.CMYK_to_CMY, color_conversions.CMY_to_RGB,
                color_conversions.RGB_to_XYZ, color_conversions.XYZ_to_Lab,
                color_conversions.Lab_to_LCHab],
      "lchuv": [color_conversions.CMYK_to_CMY, color_conversions.CMY_to_RGB,
                color_conversions.RGB_to_XYZ, color_conversions.XYZ_to_Luv,
                color_conversions.Luv_to_LCHuv],
        "luv": [color_conversions.CMYK_to_CMY, color_conversions.CMY_to_RGB,
                color_conversions.RGB_to_XYZ, color_conversions.XYZ_to_RGB],
    }
    VALUES = ['cmyk_c', 'cmyk_m', 'cmyk_y', 'cmyk_k']

    def __init__(self, cmyk_c, cmyk_m, cmyk_y, cmyk_k):
        super(CMYKColor, self).__init__()
        self.cmyk_c = float(cmyk_c)
        self.cmyk_m = float(cmyk_m)
        self.cmyk_y = float(cmyk_y)
        self.cmyk_k = float(cmyk_k)
