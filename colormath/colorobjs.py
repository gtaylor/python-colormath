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
import color_conversions
from color_exceptions import *
import constants

class ColorBase(object):
    """
    A base class holding some common methods and values.
    """
    def __init__(self):
        # This is the most common illuminant, default to it.
        self.illuminant = "D50"
        # Again, this is the most commonly used observer angle.
        self.observer = 2
        
    def convert_to(self, cs_to, debug=False, *args, **kwargs):
        """
        Converts the color to the designated colorspace.
        """
        try:
            # Look up the conversion path for the specified color space.
            conversions = self.CONVERSIONS[cs_to.lower()]
        except KeyError:
            raise InvalidConversion(self.__class__.__name__, cs_to)
        
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
            retval += '%s:%.4f ' % (val, getattr(self, val))
        return retval.strip() + ')'
    
    def has_required_values(self):
        """
        Checks all of the spectral fields to ensure there are no None values.
        """
        for field in self.VALUES:
            if field == None:
                return False
        return True
    
    def get_illuminant_xyz(self):
        """
        Returns the color's illuminant's XYZ values.
        """
        try:
            illums_observer = constants.ILLUMINANTS[str(self.observer)]
        except KeyError:
            raise InvalidObserver(self)
        
        try:
            illum_xyz = illums_observer[self.illuminant.lower()]
        except AttributeError:
            raise InvalidIlluminant(self)
        except KeyError:
            raise InvalidIlluminant(self)
        
        return illum_xyz

class SpectralColor(ColorBase):
    """
    Represents a color that may have operations done to it. You need not use
    this object with the library as long as you use all of the instance
    variables here.
    """
    CONVERSIONS = {
        "xyz": [color_conversions.Spectral_to_XYZ],
        "xyy": [color_conversions.Spectral_to_XYZ, color_conversions.XYZ_to_xyY],
        "lab": [color_conversions.Spectral_to_XYZ, color_conversions.XYZ_to_Lab],
        "lch": [color_conversions.Spectral_to_XYZ, color_conversions.XYZ_to_Lab, 
                color_conversions.Lab_to_LCH],
        "luv": [color_conversions.Spectral_to_XYZ, color_conversions.XYZ_to_Luv],
        "rgb": [color_conversions.Spectral_to_XYZ, color_conversions.XYZ_to_RGB],
    }
    VALUES = ['spec_380nm', 'spec_390nm', 
            'spec_400nm', 'spec_410nm', 'spec_420nm', 'spec_430nm',
            'spec_440nm', 'spec_450nm', 'spec_460nm', 'spec_470nm',
            'spec_480nm', 'spec_490nm', 'spec_500nm', 'spec_510nm',
            'spec_520nm', 'spec_530nm', 'spec_540nm', 'spec_550nm',
            'spec_560nm', 'spec_570nm', 'spec_580nm', 'spec_590nm',
            'spec_600nm', 'spec_610nm', 'spec_620nm', 'spec_630nm', 
            'spec_640nm', 'spec_650nm', 'spec_660nm', 'spec_670nm',
            'spec_680nm', 'spec_690nm', 'spec_700nm', 'spec_710nm',
            'spec_720nm', 'spec_730nm']
    
    def __init__(self):
        super(SpectralColor, self).__init__()
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
        
    def color_to_numpy_array(self):
        """
        Dump this color into NumPy array.
        """
        color_array = numpy.array((
            self.spec_380nm,
            self.spec_390nm,
            self.spec_400nm,
            self.spec_410nm,
            self.spec_420nm,
            self.spec_430nm,
            self.spec_440nm,
            self.spec_450nm,
            self.spec_460nm,
            self.spec_470nm,
            self.spec_480nm,
            self.spec_490nm,
            self.spec_500nm,
            self.spec_510nm,
            self.spec_520nm,
            self.spec_530nm,
            self.spec_540nm,
            self.spec_550nm,
            self.spec_560nm,
            self.spec_570nm,
            self.spec_580nm,
            self.spec_590nm,
            self.spec_600nm,
            self.spec_610nm,
            self.spec_620nm,
            self.spec_630nm,
            self.spec_640nm,
            self.spec_650nm,
            self.spec_660nm,
            self.spec_670nm,
            self.spec_680nm,
            self.spec_690nm,
            self.spec_700nm,
            self.spec_710nm,
            self.spec_720nm,
            self.spec_730nm,
        ))
        return color_array
    
class LabColor(ColorBase):
    """
    Represents an Lab color.
    """
    CONVERSIONS = {
        "xyz": [color_conversions.Lab_to_XYZ],
        "xyy": [color_conversions.Lab_to_XYZ, color_conversions.XYZ_to_xyY],
        "lch": [color_conversions.Lab_to_LCH],
        "luv": [color_conversions.Lab_to_XYZ, color_conversions.XYZ_to_Luv],
        "rgb": [color_conversions.Lab_to_XYZ, color_conversions.XYZ_to_RGB],
    }
    VALUES = ['lab_l', 'lab_a', 'lab_b']
       
    def __init__(self):
        super(LabColor, self).__init__()
        self.lab_l = None
        self.lab_a = None
        self.lab_b = None
        
class LCHColor(ColorBase):
    """
    Represents an LCH color.
    """
    CONVERSIONS = {
        "xyz": [color_conversions.LCH_to_Lab, color_conversions.Lab_to_XYZ],
        "xyy": [color_conversions.LCH_to_Lab, color_conversions.Lab_to_XYZ, 
                color_conversions.XYZ_to_xyY],
        "lab": [color_conversions.LCH_to_Lab],
        "luv": [color_conversions.LCH_to_Lab, color_conversions.Lab_to_XYZ, 
                color_conversions.XYZ_to_Luv],
        "rgb": [color_conversions.LCH_to_Lab, color_conversions.Lab_to_XYZ, 
                color_conversions.XYZ_to_RGB],
    }
    VALUES = ['lch_l', 'lch_c', 'lch_h']
    
    def __init__(self):
        super(LCHColor, self).__init__()
        self.lch_l = None
        self.lch_c = None
        self.lch_h = None
        
class LuvColor(ColorBase):
    """
    Represents an Luv color.
    """
    CONVERSIONS = {
        "xyz": [color_conversions.Luv_to_XYZ],
        "xyy": [color_conversions.Luv_to_XYZ, color_conversions.XYZ_to_xyY],
        "lab": [color_conversions.Luv_to_XYZ, color_conversions.XYZ_to_Lab],
        "lch": [color_conversions.Luv_to_XYZ, color_conversions.XYZ_to_Lab, 
                color_conversions.Lab_to_LCH],
        "rgb": [color_conversions.Luv_to_XYZ, color_conversions.XYZ_to_RGB],
    }
    VALUES = ['luv_l', 'luv_u', 'luv_v']
    
    def __init__(self):
        super(LuvColor, self).__init__()
        self.luv_l = None
        self.luv_u = None
        self.luv_v = None
        
class XYZColor(ColorBase):
    """
    Represents an XYZ color.
    """
    CONVERSIONS = {
        "xyy": [color_conversions.XYZ_to_xyY],
        "lab": [color_conversions.XYZ_to_Lab],
        "lch": [color_conversions.XYZ_to_Lab, color_conversions.Lab_to_LCH],
        "luv": [color_conversions.XYZ_to_Luv],
        "rgb": [color_conversions.XYZ_to_RGB],
    }
    VALUES = ['xyz_x', 'xyz_y', 'xyz_z']
    
    def __init__(self):
        super(XYZColor, self).__init__()
        self.xyz_x = None
        self.xyz_y = None
        self.xyz_z = None
        
class xyYColor(ColorBase):
    """
    Represents an xYy color.
    """
    CONVERSIONS = {
        "xyz": [color_conversions.xyY_to_XYZ],
        "lab": [color_conversions.xyY_to_XYZ, color_conversions.XYZ_to_Lab],
        "lch": [color_conversions.xyY_to_XYZ, color_conversions.XYZ_to_Lab, 
                color_conversions.Lab_to_LCH],
        "luv": [color_conversions.xyY_to_XYZ, color_conversions.XYZ_to_Luv],
        "rgb": [color_conversions.xyY_to_XYZ, color_conversions.XYZ_to_RGB],
    }
    VALUES = ['xyy_x', 'xyy_y', 'xyy_Y']
    
    def __init__(self):
        super(xyYColor, self).__init__()
        self.xyy_x = None
        self.xyy_y = None
        self.xyy_Y = None
        
class RGBColor(ColorBase):
    """
    Represents an Lab color.
    """
    CONVERSIONS = {
        "xyz": [color_conversions.RGB_to_XYZ],
        "xyy": [color_conversions.RGB_to_XYZ, color_conversions.XYZ_to_xyY],
        "lab": [color_conversions.RGB_to_XYZ, color_conversions.XYZ_to_Lab],
        "lch": [color_conversions.RGB_to_XYZ, color_conversions.XYZ_to_Lab, 
                color_conversions.Lab_to_LCH],
        "luv": [color_conversions.RGB_to_XYZ, color_conversions.XYZ_to_RGB],
    }
    VALUES = ['rgb_r', 'rgb_g', 'rgb_b']
    
    def __init__(self):
        super(RGBColor, self).__init__()
        self.rgb_r = None
        self.rgb_g = None
        self.rgb_b = None
        
class CMYColor(ColorBase):
    """
    Represents a CMY color.
    """
    CONVERSIONS = {
        "cmyk": [color_conversions.CMY_to_CMYK],
    }
    VALUES = ['cmy_c', 'cmy_m', 'cmy_y']
    
    def __init__(self):
        super(CMYColor, self).__init__()
        self.cmy_c = None
        self.cmy_m = None
        self.cmy_y = None
        
class CMYKColor(ColorBase):
    """
    Represents a CMYK color.
    """
    CONVERSIONS = {}
    VALUES = ['cmyk_c', 'cmyk_m', 'cmyk_y', 'cmyk_k']
    
    def __init__(self):
        super(CMYKColor, self).__init__()
        self.cmyk_c = None
        self.cmyk_m = None
        self.cmyk_y = None
        self.cmyk_k = None
        
if __name__ == "__main__":
    """
    Console testing stuff.
    """
    test = xyYColor()
    test.xyy_x = 0.468698
    test.xyy_y = 0.394554
    test.xyy_Y = 0.553500
    result = test.convert_to("lab", debug=True)
    print result