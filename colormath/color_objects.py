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
This module contains classes to represent various color spaces.
"""
import numpy
from colormath import color_conversions
from colormath.color_exceptions import *
from colormath import color_constants
from colormath.color_diff import delta_e_cie2000, delta_e_cie1976, delta_e_cie1994, delta_e_cmc

class ColorBase(object):
    """
    A base class holding some common methods and values.
    """
    def __init__(self, *args, **kwargs):
        # This is the most common illuminant, default to it.
        self.illuminant = 'd50'
        # This is the most commonly used observer angle.
        self.observer = '2'
        
    def _transfer_kwargs(self, *args, **kwargs):
        """
        Transfers any keyword arguments to the appropriate coordinate fields
        if they match one of the keys in the class's VALUES dict.
        """
        for key, val in kwargs.items():
            if key in self.VALUES:
                setattr(self, key, val)
                
    def __prep_strings(self):
        """
        Makes sure all string variables are lowercase beforehand.
        """
        self.illuminant = self.illuminant.lower()
        self.observer == str(self.observer)

    def convert_to(self, cs_to, *args, **kwargs):
        """
        Converts the color to the designated colorspace.
        """
        debug = kwargs.get('debug', False)
        try:
            # Look up the conversion path for the specified color space.
            conversions = self.CONVERSIONS[cs_to.lower()]
        except KeyError:
            raise InvalidConversion(self.__class__.__name__, cs_to)
        
        # Make sure the object has all of its required values before even
        # attempting a conversion.
        self.has_required_values()
        # Make sure any string variables are lowercase.
        self.__prep_strings()
        
        if debug:
            print 'Converting %s to %s' % (self, cs_to)
            print ' @ Conversion path: %s' % [conv.__name__ for conv in conversions]

        cobj = self
        # Iterate through the list of functions for the conversion path, storing
        # the results in a dictionary via update(). This way the user has access
        # to all of the variables involved in the conversion.
        for func in conversions:
            # Execute the function in this conversion step and store the resulting
            # Color object.
            if debug:
                print ' * Conversion: %s passed to %s()' % (
                                        cobj.__class__.__name__, func.__name__)
                print ' |->  in %s' % cobj
                
            if func:
                # This can be None if you try to convert a color to the color
                # space that is already in. IE: XYZ->XYZ.
                cobj = func(cobj, *args, **kwargs)
            
            if debug:
                print ' |-< out %s' % cobj
        return cobj
    
    def __str__(self):
        """
        String representation of the color.
        """
        retval = self.__class__.__name__ + ' ('
        for val in self.VALUES:
            value = getattr(self, val, None)
            #print "VAL: %s Type: %s" % (val, value)
            if value != None:
                retval += '%s:%.4f ' % (val, getattr(self, val))
        return retval.strip() + ')'
    
    def has_required_values(self):
        """
        Checks all of the spectral fields to ensure there are no None values.
        """
        for val in self.VALUES:
            value = getattr(self, val, None)
            if value == None:
                # A required value is missing.
                raise MissingValue(self, val)
            
            try:
                # If this fails, it's not a usable number.
                float(value)
            except ValueError:
                raise InvalidValue(self, val, value)
        return True
    
    def get_illuminant_xyz(self):
        """
        Returns the color's illuminant's XYZ values.
        """
        try:
            illums_observer = color_constants.ILLUMINANTS[str(self.observer)]
        except KeyError:
            raise InvalidObserver(self)
        
        try:
            illum_xyz = illums_observer[self.illuminant.lower()]
        except AttributeError:
            raise InvalidIlluminant(self)
        except KeyError:
            raise InvalidIlluminant(self)
        
        return illum_xyz
    
    def delta_e(self, other_color, mode='cie2000', *args, **kwargs):
        """
        Compares this color to another via Delta E.
        
        Valid modes:
         cie2000
         cie1976
        """
        if not isinstance(other_color, ColorBase):
            raise InvalidArgument('delta_e_cie2000', 'other_color', other_color)
        
        # Convert the colors to Lab if they are not already.
        lab1 = self.convert_to('lab')
        lab2 = other_color.convert_to('lab')
        
        mode = mode.lower()
        if mode == 'cie2000':
            return delta_e_cie2000(lab1, lab2)
        elif mode == 'cie1994':
            return delta_e_cie1994(lab1, lab2, **kwargs)
        elif mode == 'cie1976':
            return delta_e_cie1976(lab1, lab2)
        elif mode == 'cmc':
            return delta_e_cmc(lab1, lab2, **kwargs)
        else:
            raise InvalidDeltaEMode(mode)

class SpectralColor(ColorBase):
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
    }
    VALUES = ['spec_380nm', 'spec_390nm', 'spec_400nm', 'spec_410nm', 
              'spec_420nm', 'spec_430nm', 'spec_440nm', 'spec_450nm', 
              'spec_460nm', 'spec_470nm', 'spec_480nm', 'spec_490nm', 
              'spec_500nm', 'spec_510nm', 'spec_520nm', 'spec_530nm', 
              'spec_540nm', 'spec_550nm', 'spec_560nm', 'spec_570nm', 
              'spec_580nm', 'spec_590nm', 'spec_600nm', 'spec_610nm', 
              'spec_620nm', 'spec_630nm', 'spec_640nm', 'spec_650nm', 
              'spec_660nm', 'spec_670nm', 'spec_680nm', 'spec_690nm', 
              'spec_700nm', 'spec_710nm', 'spec_720nm', 'spec_730nm']
    
    def __init__(self, *args, **kwargs):
        super(SpectralColor, self).__init__(*args, **kwargs)
        # Spectral fields
        self.spec_380nm = None # begin Blue wavelengths
        self.spec_390nm = None
        self.spec_400nm = None
        self.spec_410nm = None
        self.spec_420nm = None
        self.spec_430nm = None
        self.spec_440nm = None
        self.spec_450nm = None
        self.spec_460nm = None
        self.spec_470nm = None
        self.spec_480nm = None
        self.spec_490nm = None # end Blue wavelengths
        self.spec_500nm = None # start Green wavelengths
        self.spec_510nm = None
        self.spec_520nm = None
        self.spec_530nm = None
        self.spec_540nm = None
        self.spec_550nm = None
        self.spec_560nm = None
        self.spec_570nm = None
        self.spec_580nm = None
        self.spec_590nm = None
        self.spec_600nm = None
        self.spec_610nm = None # end Green wavelengths
        self.spec_620nm = None # start Red wavelengths
        self.spec_630nm = None
        self.spec_640nm = None
        self.spec_650nm = None
        self.spec_660nm = None
        self.spec_670nm = None
        self.spec_680nm = None
        self.spec_690nm = None
        self.spec_700nm = None
        self.spec_710nm = None
        self.spec_720nm = None
        self.spec_730nm = None # end Red wavelengths
        self._transfer_kwargs(*args, **kwargs)
        
    def get_numpy_array(self):
        """
        Dump this color into NumPy array.
        """
        color_array = numpy.array((self.spec_380nm, self.spec_390nm,
            self.spec_400nm, self.spec_410nm, self.spec_420nm, self.spec_430nm,
            self.spec_440nm, self.spec_450nm, self.spec_460nm, self.spec_470nm,
            self.spec_480nm, self.spec_490nm, self.spec_500nm, self.spec_510nm,
            self.spec_520nm, self.spec_530nm, self.spec_540nm, self.spec_550nm,
            self.spec_560nm, self.spec_570nm, self.spec_580nm, self.spec_590nm,
            self.spec_600nm, self.spec_610nm, self.spec_620nm, self.spec_630nm,
            self.spec_640nm, self.spec_650nm, self.spec_660nm, self.spec_670nm,
            self.spec_680nm, self.spec_690nm, self.spec_700nm, self.spec_710nm,
            self.spec_720nm, self.spec_730nm))
        return color_array
    
class LabColor(ColorBase):
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
    }
    VALUES = ['lab_l', 'lab_a', 'lab_b']
       
    def __init__(self, *args, **kwargs):
        super(LabColor, self).__init__(*args, **kwargs)
        self.lab_l = None
        self.lab_a = None
        self.lab_b = None
        self._transfer_kwargs(*args, **kwargs)
        
class LCHabColor(ColorBase):
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
    }
    VALUES = ['lch_l', 'lch_c', 'lch_h']
    
    def __init__(self, *args, **kwargs):
        super(LCHabColor, self).__init__(*args, **kwargs)
        self.lch_l = None
        self.lch_c = None
        self.lch_h = None
        self._transfer_kwargs(*args, **kwargs)
        
class LCHuvColor(ColorBase):
    """
    Represents an LCHuv color.
    """
    CONVERSIONS = {
      "lchuv": [None],
        "xyz": [color_conversions.LCHuv_to_Luv, color_conversions.Lab_to_XYZ],
        "xyy": [color_conversions.LCHuv_to_Luv, color_conversions.Lab_to_XYZ, 
                color_conversions.XYZ_to_xyY],
        "lab": [color_conversions.LCHuv_to_Luv, color_conversions.Luv_to_XYZ, 
                color_conversions.XYZ_to_Lab],
        "luv": [color_conversions.LCHuv_to_Luv],
      "lchab": [color_conversions.LCHuv_to_Luv, color_conversions.Luv_to_XYZ,
                color_conversions.XYZ_to_Lab, color_conversions.Lab_to_LCHab],
        "rgb": [color_conversions.LCHuv_to_Luv, color_conversions.Luv_to_XYZ, 
                color_conversions.XYZ_to_RGB],
    }
    VALUES = ['lch_l', 'lch_c', 'lch_h']
    
    def __init__(self, *args, **kwargs):
        super(LCHuvColor, self).__init__(*args, **kwargs)
        self.lch_l = None
        self.lch_c = None
        self.lch_h = None
        self._transfer_kwargs(*args, **kwargs)
        
class LuvColor(ColorBase):
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
    }
    VALUES = ['luv_l', 'luv_u', 'luv_v']
    
    def __init__(self, *args, **kwargs):
        super(LuvColor, self).__init__(*args, **kwargs)
        self.luv_l = None
        self.luv_u = None
        self.luv_v = None
        self._transfer_kwargs(*args, **kwargs)
        
class XYZColor(ColorBase):
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
    }
    VALUES = ['xyz_x', 'xyz_y', 'xyz_z']
    
    def __init__(self, *args, **kwargs):
        super(XYZColor, self).__init__(*args, **kwargs)
        self.xyz_x = None
        self.xyz_y = None
        self.xyz_z = None
        self._transfer_kwargs(*args, **kwargs)
        
class xyYColor(ColorBase):
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
    }
    VALUES = ['xyy_x', 'xyy_y', 'xyy_Y']
    
    def __init__(self, *args, **kwargs):
        super(xyYColor, self).__init__(*args, **kwargs)
        self.xyy_x = None
        self.xyy_y = None
        self.xyy_Y = None
        self._transfer_kwargs(*args, **kwargs)
        
class RGBColor(ColorBase):
    """
    Represents an Lab color.
    """
    CONVERSIONS = {
        "rgb": [None],
        "xyz": [color_conversions.RGB_to_XYZ],
        "xyy": [color_conversions.RGB_to_XYZ, color_conversions.XYZ_to_xyY],
        "lab": [color_conversions.RGB_to_XYZ, color_conversions.XYZ_to_Lab],
      "lchab": [color_conversions.RGB_to_XYZ, color_conversions.XYZ_to_Lab, 
                color_conversions.Lab_to_LCHab],
      "lchuv": [color_conversions.RGB_to_XYZ, color_conversions.XYZ_to_Luv, 
                color_conversions.Luv_to_LCHuv],
        "luv": [color_conversions.RGB_to_XYZ, color_conversions.XYZ_to_RGB],
    }
    VALUES = ['rgb_r', 'rgb_g', 'rgb_b']
    
    def __init__(self, *args, **kwargs):
        super(RGBColor, self).__init__(*args, **kwargs)
        self.rgb_r = None
        self.rgb_g = None
        self.rgb_b = None
        self.rgb_type = 'srgb'
        self._transfer_kwargs(*args, **kwargs)
        
    def __str__(self):
        parent_str = super(RGBColor, self).__str__()
        return '%s [%s]' % (parent_str, self.rgb_type)
        
class CMYColor(ColorBase):
    """
    Represents a CMY color.
    """
    CONVERSIONS = {
        "cmy": [None],
       "cmyk": [color_conversions.CMY_to_CMYK],
    }
    VALUES = ['cmy_c', 'cmy_m', 'cmy_y']
    
    def __init__(self, *args, **kwargs):
        super(CMYColor, self).__init__(*args, **kwargs)
        self.cmy_c = None
        self.cmy_m = None
        self.cmy_y = None
        self._transfer_kwargs(*args, **kwargs)
        
class CMYKColor(ColorBase):
    """
    Represents a CMYK color.
    """
    CONVERSIONS = {
       "cmyk": [None],
    }
    VALUES = ['cmyk_c', 'cmyk_m', 'cmyk_y', 'cmyk_k']
    
    def __init__(self, *args, **kwargs):
        super(CMYKColor, self).__init__(*args, **kwargs)
        self.cmyk_c = None
        self.cmyk_m = None
        self.cmyk_y = None
        self.cmyk_k = None
        self._transfer_kwargs(*args, **kwargs)