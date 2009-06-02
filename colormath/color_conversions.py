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
Conversion between color spaces
"""
import math
import numpy
from colormath import color_constants
from colormath import spectral_constants
from colormath.color_exceptions import InvalidIlluminant

def _transfer_common(old_cobj, new_cobj):
    """
    Transfer illuminant and observer data to a new color object. This is
    """
    new_cobj.illuminant = old_cobj.illuminant
    new_cobj.observer = old_cobj.observer

def apply_XYZ_transformation(val_x, val_y, val_z, orig_illum, targ_illum, 
                             adaptation="bradford", debug=False):
    """
    Applies an XYZ transformation matrix to convert XYZ values between
    illuminants. It is important to recognize that color transformation results
    in color errors, determined by how far the original illuminant is from the
    target illuminant. For example, D65 to A could result in very high maximum
    deviances. 
    """
    orig_illum = orig_illum.lower()
    targ_illum = targ_illum.lower()
    adaptation = adaptation.lower()
   
    if debug:
        print "  \* Applying adaptation matrix: %s" % adaptation
    # Retrieve the appropriate transformation matrix from the constants.
    transform_matrix = color_constants.ADAPTATION_MATRICES[orig_illum][targ_illum][adaptation]

    # Stuff the XYZ values into a NumPy matrix for conversion.
    XYZ_matrix = numpy.array((
        val_x, val_y, val_z
     ))
    # Perform the adaptation via matrix multiplication.
    result_matrix = numpy.dot(XYZ_matrix, transform_matrix)
    return result_matrix[0], result_matrix[1], result_matrix[2]

def apply_RGB_matrix(var1, var2, var3, rgb_type, convtype="xyz_to_rgb", 
                     debug=False):
    """
    Applies an RGB working matrix to convert from XYZ to RGB.
    The arguments are tersely named var1, var2, and var3 to allow for the passing
    of XYZ _or_ RGB values. var1 is X for XYZ, and R for RGB. var2 and var3
    follow suite.
    """
    rgb_type = rgb_type.lower()
    convtype = convtype.lower()
    # Retrieve the appropriate transformation matrix from the constants.
    rgb_matrix = color_constants.RGB_SPECS[rgb_type]["conversions"][convtype]
   
    if debug:
        print "  \* Applying RGB conversion matrix: %s->%s" % (rgb_type, convtype)
    # Stuff the RGB/XYZ values into a NumPy matrix for conversion.
    var_matrix = numpy.array((
        var1, var2, var3
    ))
    # Perform the adaptation via matrix multiplication.
    result_matrix = numpy.dot(var_matrix, rgb_matrix)
    return result_matrix[0], result_matrix[1], result_matrix[2]

def Spectral_to_XYZ(cobj, debug=False, illuminant_override=None, *args, **kwargs):
    """
    Converts spectral readings to XYZ.
    """
    xyzcolor = color_objects.XYZColor()
    _transfer_common(cobj, xyzcolor)
    
    # If the user provides an illuminant_override numpy array, use it.
    if illuminant_override:
        reference_illum = illuminant_override
    else:
        # Otherwise, look up the illuminant from known standards based
        # on the value of 'illuminant' pulled from the SpectralColor object.
        try:
            reference_illum = spectral_constants.REF_ILLUM_TABLE[cobj.illuminant]
        except KeyError:
            raise InvalidIlluminant(cobj)
        
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
    
    xyzcolor.xyz_x = x_numerator.sum() / denom.sum()
    xyzcolor.xyz_y = y_numerator.sum() / denom.sum()
    xyzcolor.xyz_z = z_numerator.sum() / denom.sum()
    
    return xyzcolor

def Lab_to_LCHab(cobj, debug=False, *args, **kwargs):
    """
    Convert from CIE Lab to LCH(ab).
    """
    lchcolor = color_objects.LCHabColor()
    _transfer_common(cobj, lchcolor)
   
    lchcolor.lch_l = cobj.lab_l
    lchcolor.lch_c = math.sqrt(math.pow(float(cobj.lab_a),2) + math.pow(float(cobj.lab_b),2))
    lchcolor.lch_h = math.atan2(float(cobj.lab_b), float(cobj.lab_a))
   
    if (lchcolor.lch_h > 0):
        lchcolor.lch_h = (lchcolor.lch_h / math.pi) * 180
    else:
        lchcolor.lch_h = 360 - (math.fabs(lchcolor.lch_h) / math.pi) * 180
      
    return lchcolor

def Lab_to_XYZ(cobj, debug=False, *args, **kwargs):
    """
    Convert from Lab to XYZ
    """
    illum = cobj.get_illuminant_xyz()
    xyzcolor = color_objects.XYZColor()
    _transfer_common(cobj, xyzcolor)
   
    xyzcolor.xyz_y = (cobj.lab_l + 16.0) / 116.0
    xyzcolor.xyz_x = cobj.lab_a / 500.0 + xyzcolor.xyz_y
    xyzcolor.xyz_z = xyzcolor.xyz_y - cobj.lab_b / 200.0
   
    if math.pow(xyzcolor.xyz_y, 3) > color_constants.CIE_E:
        xyzcolor.xyz_y = math.pow(xyzcolor.xyz_y, 3)
    else:
        xyzcolor.xyz_y = (xyzcolor.xyz_y - 16.0 / 116.0) / 7.787

    if math.pow(xyzcolor.xyz_x, 3) > color_constants.CIE_E:
        xyzcolor.xyz_x = math.pow(xyzcolor.xyz_x, 3)
    else:
        xyzcolor.xyz_x = (xyzcolor.xyz_x - 16.0 / 116.0) / 7.787
      
    if math.pow(xyzcolor.xyz_z, 3) > color_constants.CIE_E:
        xyzcolor.xyz_z = math.pow(xyzcolor.xyz_z, 3)
    else:
        xyzcolor.xyz_z = (xyzcolor.xyz_z - 16.0 / 116.0) / 7.787
      
    xyzcolor.xyz_x = (illum["X"] * xyzcolor.xyz_x)
    xyzcolor.xyz_y = (illum["Y"] * xyzcolor.xyz_y)
    xyzcolor.xyz_z = (illum["Z"] * xyzcolor.xyz_z)
    
    return xyzcolor

def Luv_to_LCHuv(cobj, debug=False, *args, **kwargs):
    """
    Convert from CIE Luv to LCH(uv).
    """
    lchcolor = color_objects.LCHuvColor()
    _transfer_common(cobj, lchcolor)
   
    lchcolor.lch_l = cobj.luv_l
    lchcolor.lch_c = math.sqrt(math.pow(cobj.luv_u, 2.0) + math.pow(cobj.luv_v, 2.0))
    lchcolor.lch_h = math.atan2(float(cobj.luv_v), float(cobj.luv_u))
   
    if lchcolor.lch_h > 0:
        lchcolor.lch_h = (lchcolor.lch_h / math.pi) * 180
    else:
        lchcolor.lch_h = 360 - (math.fabs(lchcolor.lch_h) / math.pi) * 180
    return lchcolor

def Luv_to_XYZ(cobj, debug=False, *args, **kwargs):
    """
    Convert from Luv to XYZ.
    """
    xyzcolor = color_objects.XYZColor()
    _transfer_common(cobj, xyzcolor)
    illum = xyzcolor.get_illuminant_xyz()
   
    # Various variables used throughout the conversion.
    cie_k_times_e = color_constants.CIE_K * color_constants.CIE_E
    u_sub_0 = (4.0 * illum["X"]) / (illum["X"] + 15.0 * illum["Y"] + 3.0 * illum["Z"])
    v_sub_0 = (9.0 * illum["Y"]) / (illum["X"] + 15.0 * illum["Y"] + 3.0 * illum["Z"])
    var_a_frac = (52.0 * cobj.luv_l) / (cobj.luv_u + 13.0 * cobj.luv_l * u_sub_0) 
    var_a = (1.0/3.0) * (var_a_frac - 1.0)
    var_c = -(1.0/3.0)
   
    # Y-coordinate calculations.
    if cobj.luv_l > cie_k_times_e:
        xyzcolor.xyz_y = math.pow((cobj.luv_l + 16.0) / 116.0, 3.0)
    else:
        xyzcolor.xyz_y = cobj.luv_l / color_constants.CIE_K
      
    # These variables depend on Y-coordinate being solved.
    var_b = -5.0 * xyzcolor.xyz_y 
    var_d_frac = (39.0 * cobj.luv_l) / (cobj.luv_v + 13.0 * cobj.luv_l * v_sub_0)
    var_d = xyzcolor.xyz_y * (var_d_frac - 5.0)
   
    # X-coordinate calculation.
    xyzcolor.xyz_x = (var_d - var_b) / (var_a - var_c)
    # Z-coordinate calculation.
    xyzcolor.xyz_z = xyzcolor.xyz_x * var_a + var_b
   
    # Scale the values up.
    xyzcolor.xyz_x *= 100.0
    xyzcolor.xyz_y *= 100.0
    xyzcolor.xyz_z *= 100.0
   
    return xyzcolor

def LCHab_to_Lab(cobj, debug=False, *args, **kwargs):
    """
    Convert from LCH(ab) to Lab.
    """
    labcolor = color_objects.LabColor()
    _transfer_common(cobj, labcolor)
   
    labcolor.lab_l = float(cobj.lch_l)
    labcolor.lab_a = math.cos(math.radians(cobj.lch_h)) * float(cobj.lch_c)
    labcolor.lab_b = math.sin(math.radians(cobj.lch_h)) * float(cobj.lch_c)
    return labcolor

def LCHuv_to_Luv(cobj, debug=False, *args, **kwargs):
    """
    Convert from LCH(uv) to Luv.
    """
    luvcolor = color_objects.LuvColor()
    _transfer_common(cobj, luvcolor)
   
    luvcolor.luv_l = float(cobj.lch_l)
    luvcolor.luv_u = math.cos(math.radians(cobj.lch_h)) * float(cobj.lch_c)
    luvcolor.luv_v = math.sin(math.radians(cobj.lch_h)) * float(cobj.lch_c)
    return luvcolor

def xyY_to_XYZ(cobj, debug=False, *args, **kwargs):
    """
    Convert from xyY to XYZ.
    """
    xyzcolor = color_objects.XYZColor()
    _transfer_common(cobj, xyzcolor)
   
    xyzcolor.xyz_x = (cobj.xyy_x * cobj.xyy_Y) / (cobj.xyy_y)
    xyzcolor.xyz_y = cobj.xyy_Y
    xyzcolor.xyz_z = ((1.0 - cobj.xyy_x - cobj.xyy_y) * xyzcolor.xyz_y) / (cobj.xyy_y)
    
    return xyzcolor

def XYZ_to_xyY(cobj, debug=False, *args, **kwargs):
    """
    Convert from XYZ to xyY.
    """
    xyycolor = color_objects.xyYColor()
    _transfer_common(cobj, xyycolor)
   
    xyycolor.xyy_x = (cobj.xyz_x) / (cobj.xyz_x + cobj.xyz_y + cobj.xyz_z)
    xyycolor.xyy_y = (cobj.xyz_y) / (cobj.xyz_x + cobj.xyz_y + cobj.xyz_z)
    xyycolor.xyy_Y = cobj.xyz_y

    return xyycolor

def XYZ_to_Luv(cobj, debug=False, *args, **kwargs):
    """
    Convert from XYZ to Luv
    """
    luvcolor = color_objects.LuvColor()
    _transfer_common(cobj, luvcolor)
   
    temp_x = cobj.xyz_x
    temp_y = cobj.xyz_y
    temp_z = cobj.xyz_z
   
    luvcolor.luv_u = (4.0 * temp_x) / (temp_x + (15.0 * temp_y) + (3.0 * temp_z))
    luvcolor.luv_v = (9.0 * temp_y) / (temp_x + (15.0 * temp_y) + (3.0 * temp_z))

    illum = luvcolor.get_illuminant_xyz()  
    temp_y = temp_y / illum["Y"]
    if temp_y > color_constants.CIE_E:
        temp_y = math.pow(temp_y, (1.0 / 3.0))
    else:
        temp_y = (7.787 * temp_y) + (16.0 / 116.0)
   
    ref_U = (4.0 * illum["X"]) / (illum["X"] + (15.0 * illum["Y"]) + (3.0 * illum["Z"]))
    ref_V = (9.0 * illum["Y"]) / (illum["X"] + (15.0 * illum["Y"]) + (3.0 * illum["Z"]))
   
    luvcolor.luv_l = (116.0 * temp_y) - 16.0
    luvcolor.luv_u = 13.0 * luvcolor.luv_l * (luvcolor.luv_u - ref_U)
    luvcolor.luv_v = 13.0 * luvcolor.luv_l * (luvcolor.luv_v - ref_V)
   
    return luvcolor

def XYZ_to_Lab(cobj, debug=False, *args, **kwargs):
    """
    Converts XYZ to Lab.
    """
    illum = cobj.get_illuminant_xyz()
    labcolor = color_objects.LabColor()
    _transfer_common(cobj, labcolor)
   
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
      
    labcolor.lab_l = (116.0 * temp_y) - 16.0
    labcolor.lab_a = 500.0 * (temp_x - temp_y)
    labcolor.lab_b = 200.0 * (temp_y - temp_z)
    return labcolor

def __downscale_rgb_vals(r, g, b):
    """
    Scales an RGB color object from an int 0-255 to decimal 0.0-1.0.
    """
    var_r = r / 255.0
    var_g = g / 255.0
    var_b = b / 255.0
    
    return (var_r, var_g, var_b)

def __upscale_rgb(rgbcolor):
    """
    Scales an RGB color object from decimal 0.0-1.0 to int 0-255.
    """
    # RGB values are to not go under 0.
    if rgbcolor.rgb_r < 0:
        rgbcolor.rgb_r = 0
    if rgbcolor.rgb_g < 0:
        rgbcolor.rgb_g = 0
    if rgbcolor.rgb_b < 0:
        rgbcolor.rgb_b = 0
      
    # Scale up to 0-255 values.
    rgbcolor.rgb_r = int(math.floor(0.5 + rgbcolor.rgb_r * 255))
    rgbcolor.rgb_g = int(math.floor(0.5 + rgbcolor.rgb_g * 255))
    rgbcolor.rgb_b = int(math.floor(0.5 + rgbcolor.rgb_b * 255))
   
    # Cap RGB values at 255. This shouldn't happen, but it's here just in case
    # things go out of gamut or other fun things.
    if rgbcolor.rgb_r > 255:
        rgbcolor.rgb_r = 255
    if rgbcolor.rgb_g > 255:
        rgbcolor.rgb_g = 255
    if rgbcolor.rgb_b > 255:
        rgbcolor.rgb_b = 255
        
    return rgbcolor

def XYZ_to_RGB(cobj, target_rgb="sRGB", debug=False, *args, **kwargs):
    """
    XYZ to RGB conversion.
    """
    target_rgb = target_rgb.lower()
    rgbcolor = color_objects.RGBColor()
    _transfer_common(cobj, rgbcolor)
    
    temp_X = cobj.xyz_x / 100.0
    temp_Y = cobj.xyz_y / 100.0
    temp_Z = cobj.xyz_z / 100.0
   
    if debug:
        print "  \- Target RGB space: %s" % target_rgb
    target_illum = color_constants.RGB_SPECS[target_rgb]["native_illum"]
    cobj.illuminant = cobj.illuminant.lower()
    if debug:
        print "  \- Target native illuminant: %s" % target_illum
        print "  \- XYZ color's illuminant: %s" % cobj.illuminant
   
    # If the XYZ values were taken with a different reference white than the
    # native reference white of the target RGB space, a transformation matrix
    # must be applied.
    if cobj.illuminant != target_illum:
        if debug:
            print "  \* Applying transformation from %s to %s " % (cobj.illuminant,
                                                                target_illum)
        # Get the adjusted XYZ values, adapted for the target illuminant.
        temp_X, temp_Y, temp_Z = apply_XYZ_transformation(temp_X, temp_Y, temp_Z, 
                                                        orig_illum=cobj.illuminant, 
                                                        targ_illum=target_illum,
                                                        debug=debug)
   
    # Apply an RGB working space matrix to the XYZ values (matrix mul).
    rgbcolor.rgb_r, rgbcolor.rgb_g, rgbcolor.rgb_b = apply_RGB_matrix(temp_X, 
                                          temp_Y, temp_Z, rgb_type=target_rgb, 
                                          convtype="xyz_to_rgb", debug=debug)

    if target_rgb == "srgb":
        # If it's sRGB...
        if rgbcolor.rgb_r > 0.0031308:
            rgbcolor.rgb_r = (1.055 * math.pow(rgbcolor.rgb_r, 1.0 / 2.4)) - 0.055
        else:
            rgbcolor.rgb_r = rgbcolor.rgb_r * 12.92
   
        if rgbcolor.rgb_g > 0.0031308:
            rgbcolor.rgb_g = (1.055 * math.pow(rgbcolor.rgb_g, 1.0 / 2.4)) - 0.055
        else:
            rgbcolor.rgb_g = rgbcolor.rgb_g * 12.92
   
        if rgbcolor.rgb_b > 0.0031308:
            rgbcolor.rgb_b = (1.055 * math.pow(rgbcolor.rgb_b, 1.0 / 2.4)) - 0.055
        else:
            rgbcolor.rgb_b = rgbcolor.rgb_b * 12.92
    else:
        # If it's not sRGB...
        gamma = color_constants.RGB_SPECS[target_rgb]["gamma"]
      
        if rgbcolor.rgb_r < 0:
            rgbcolor.rgb_r = 0
        if rgbcolor.rgb_g < 0:
            rgbcolor.rgb_g = 0
        if rgbcolor.rgb_b < 0:
            rgbcolor.rgb_b = 0
      
        #print "RGB", rgbcolor.rgb_r, rgbcolor.rgb_g, rgbcolor.rgb_b
        rgbcolor.rgb_r = math.pow(rgbcolor.rgb_r, (1 / gamma))
        rgbcolor.rgb_g = math.pow(rgbcolor.rgb_g, (1 / gamma))
        rgbcolor.rgb_b = math.pow(rgbcolor.rgb_b, (1 / gamma))
      
    rgbcolor.rgb_type = target_rgb
    return __upscale_rgb(rgbcolor)

def RGB_to_XYZ(cobj, target_illuminant=None, debug=False, *args, **kwargs):
    """
    RGB to XYZ conversion. Expects 1-255 RGB values.
    """
    xyzcolor = color_objects.XYZColor()
    _transfer_common(cobj, xyzcolor)
    
    temp_R, temp_G, temp_B = __downscale_rgb_vals(cobj.rgb_r,
                                                  cobj.rgb_g,
                                                  cobj.rgb_b)
   
    if cobj.rgb_type == "srgb":
        # If it's sRGB...
        if temp_R > 0.04045:
            temp_R = math.pow((temp_R + 0.055) / 1.055, 2.4)
        else:
            temp_R = temp_R / 12.92
   
        if temp_G > 0.04045:
            temp_G = math.pow((temp_G + 0.055) / 1.055, 2.4)
        else:
            temp_G = temp_G / 12.92
   
        if temp_B > 0.04045:
            temp_B = math.pow((temp_B + 0.055) / 1.055, 2.4)
        else:
            temp_B = temp_B / 12.92
    else:
        # If it's not sRGB...
        gamma = color_constants.RGB_SPECS[cobj.rgb_type]["gamma"]
            
        temp_R = math.pow(temp_R, gamma)
        temp_G = math.pow(temp_G, gamma)
        temp_B = math.pow(temp_B, gamma)
        
    # Apply an RGB working space matrix to the XYZ values (matrix mul).
    xyzcolor.xyz_x, xyzcolor.xyz_y, xyzcolor.xyz_z = apply_RGB_matrix(temp_R, 
                                          temp_G, temp_B, rgb_type=cobj.rgb_type, 
                                          convtype="rgb_to_xyz", debug=debug)
    
    if target_illuminant == None:
        target_illuminant = color_constants.RGB_SPECS[cobj.rgb_type]["native_illum"]
        
    # The illuminant of the original RGB object.
    source_illuminant = color_constants.RGB_SPECS[cobj.rgb_type]["native_illum"]
    
    # This needs to be correct before the adaptation is applied.
    xyzcolor.illuminant = source_illuminant
    # This will take care of any illuminant changes for us.
    xyzcolor.apply_adaptation(target_illuminant)

    return xyzcolor

def RGB_to_HSL(cobj, debug=False, *args, **kwargs):
    """
    Converts from RGB to HSL.
    
    H values are in degrees and are 0-360.
    S values are a percentage, 0.0 to 1.0.
    L values are a percentage, 0.0 to 1.0.
    """
    hslcolor = color_objects.HSLColor()
    _transfer_common(cobj, hslcolor)
    
    var_R = cobj.rgb_r / 255.0
    var_G = cobj.rgb_g / 255.0
    var_B = cobj.rgb_b / 255.0
    
    var_max = max(var_R, var_G, var_B)
    var_min = min(var_R, var_G, var_B)
    
    if var_max == var_min:
        var_H = 0
    elif var_max == var_R:
        var_H = (60.0 * ((var_G - var_B) / (var_max - var_min)) + 360) % 360.0
    elif var_max == var_G:
        var_H = 60.0 * ((var_B - var_R) / (var_max - var_min)) + 120
    elif var_max == var_B:
        var_H = 60.0 * ((var_R - var_G) / (var_max - var_min)) + 240.0
        
    var_L = 1.0 / 2.0 * (var_max + var_min)
    
    if var_max == var_min:
        var_S = 0
    elif var_L <= (1.0 / 2.0):
        var_S = (var_max - var_min) / (2.0 * var_L)
    else:
        var_S = (var_max - var_min) / (2.0 - (2.0 * var_L))
    
    target_rgb = kwargs.get('target_rgb', None)
    # Use this if it's there.
    if target_rgb != None:
        hslcolor.rgb_type = target_rgb
    else:
        hslcolor.rgb_type = cobj.rgb_type

    hslcolor.hsl_h = var_H
    hslcolor.hsl_s = var_S
    hslcolor.hsl_l = var_L
    
    return hslcolor

def __Hue_to_RGB(v1, v2, vH):
    """
    Internal function used in converting HSL's H coordinate to
    R, G, and B coordinates. 
    """
    if vH < 0:
        vH += 1
    if vH > 1:
        vH -= 1
    if (6 * vH) < 1:
        return v1 + (v2 - v1) * 6 * vH
    if (2 * vH) < 1:
        return v2
    if (3 * vH) < 2:
        return v1 + (v2 - v1) * ((2 / 3) - vH) * 6
    return v1

def HSL_to_RGB(cobj, debug=False, *args, **kwargs):
    """
    HSL to RGB conversion.
    """
    rgbcolor = color_objects.RGBColor()
    _transfer_common(cobj, rgbcolor)
    
    H = cobj.hsl_h
    S = cobj.hsl_s
    L = cobj.hsl_l
    
    # HSL from 0 to 1
    if S == 0:
        # RGB results from 0 to 255
        R = L * 255
        G = L * 255
        B = L * 255
    else:
        if L < 0.5:
            var_2 = L * (1 + S)
        else:
            var_2 = (L + S) - (S * L)
    
        var_1 = 2 * L - var_2
    
        R = 255 * __Hue_to_RGB(var_1, var_2, H + (1 / 3))
        G = 255 * __Hue_to_RGB(var_1, var_2, H)
        B = 255 * __Hue_to_RGB(var_1, var_2, H - (1 / 3))
        
    rgbcolor.rgb_r = R
    rgbcolor.rgb_g = G
    rgbcolor.rgb_b = B
    
    return rgbcolor

def RGB_to_CMY(cobj, debug=False, *args, **kwargs):
    """
    RGB to CMY conversion.
    
    NOTE: CMYK and CMY values range from 0.0 to 1.0
    """
    cmycolor = color_objects.CMYColor()
    _transfer_common(cobj, cmycolor)
   
    cmycolor.cmy_c = 1.0 - (cobj.rgb_r / 255.0)
    cmycolor.cmy_m = 1.0 - (cobj.rgb_g / 255.0)
    cmycolor.cmy_y = 1.0 - (cobj.rgb_b / 255.0)
    
    return cmycolor

def CMY_to_RGB(cobj, debug=False, *args, **kwargs):
    """
    Converts CMY to RGB via simple subtraction.
    
    NOTE: Returned values are in the range of 0-255.
    """
    rgbcolor = color_objects.RGBColor()
    _transfer_common(cobj, rgbcolor)
    
    rgbcolor.rgb_r = 1.0 - cobj.cmy_c
    rgbcolor.rgb_g = 1.0 - cobj.cmy_m
    rgbcolor.rgb_b = 1.0 - cobj.cmy_y
    
    return __upscale_rgb(rgbcolor)

def CMY_to_CMYK(cobj, debug=False, *args, **kwargs):
    """
    Converts from CMY to CMYK.
    
    NOTE: CMYK and CMY values range from 0.0 to 1.0
    """ 
    cmykcolor = color_objects.CMYKColor()
    _transfer_common(cobj, cmykcolor)
   
    var_k = 1.0
    if cobj.cmy_c < var_k:
        var_k = cobj.cmy_c
    if cobj.cmy_m < var_k:
        var_k = cobj.cmy_m
    if cobj.cmy_y < var_k:
        var_k = cobj.cmy_y
      
    if var_k == 1:
        cmykcolor.cmyk_c = 0.0
        cmykcolor.cmyk_m = 0.0
        cmykcolor.cmyk_y = 0.0
    else:
        cmykcolor.cmyk_c = (cobj.cmy_c - var_k) / (1.0 - var_k)
        cmykcolor.cmyk_m = (cobj.cmy_m - var_k) / (1.0 - var_k)
        cmykcolor.cmyk_y = (cobj.cmy_y - var_k) / (1.0 - var_k)
    cmykcolor.cmyk_k = var_k

    return cmykcolor

def CMYK_to_CMY(cobj, debug=False, *args, **kwargs):
    """
    Converts CMYK to CMY.
    
    NOTE: CMYK and CMY values range from 0.0 to 1.0
    """
    cmycolor = color_objects.CMYColor()
    _transfer_common(cobj, cmycolor)
    
    cmycolor.cmy_c = cobj.cmyk_c * (1.0 - cobj.cmyk_k) + cobj.cmyk_k
    cmycolor.cmy_m = cobj.cmyk_m * (1.0 - cobj.cmyk_k) + cobj.cmyk_k
    cmycolor.cmy_y = cobj.cmyk_y * (1.0 - cobj.cmyk_k) + cobj.cmyk_k
    
    return cmycolor

import color_objects