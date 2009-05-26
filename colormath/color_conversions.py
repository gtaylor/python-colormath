"""
Conversion between color spaces
"""
import math
import numpy
from colormath import color_constants

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
   # Return the results
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
   # Build a result dictionary from the matrix.
   return result_matrix[0], result_matrix[1], result_matrix[2]

def Spectral_to_XYZ(cobj, cdict):
   """
   Converts spectral readings to XYZ.
   """
   xyzcolor = color_objects.XYZColor()
   _transfer_common(cobj, xyzcolor)
   
   illuminants = color_constants.SPECTRAL_DISTS[str(cobj.observer)][cobj.illuminant.lower()]
   sample = cobj.color_to_numpy_array()
   xyzcolor.xyz_x = float(numpy.dot(sample, illuminants["X"]) / 100.0)
   xyzcolor.xyz_y = float(numpy.dot(sample, illuminants["Y"]) / 100.0)
   xyzcolor.xyz_z = float(numpy.dot(sample, illuminants["Z"]) / 100.0)
   return xyzcolor

def Lab_to_LCHab(cobj):
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

def Lab_to_XYZ(cobj):
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

def Luv_to_LCHuv(cobj):
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

def Luv_to_XYZ(cobj):
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

def LCHab_to_Lab(cobj):
   """
   Convert from LCH(ab) to Lab.
   """
   labcolor = color_objects.LabColor()
   _transfer_common(cobj, labcolor)
   
   labcolor.lab_l = float(cobj.lch_l)
   labcolor.lab_a = math.cos(math.radians(cobj.lch_h)) * float(cobj.lch_c)
   labcolor.lab_b = math.sin(math.radians(cobj.lch_h)) * float(cobj.lch_c)
   return labcolor

def LCHuv_to_Luv(cobj):
   """
   Convert from LCH(uv) to Luv.
   """
   luvcolor = color_objects.LuvColor()
   _transfer_common(cobj, luvcolor)
   
   luvcolor.luv_l = float(cobj.lch_l)
   luvcolor.luv_u = math.cos(math.radians(cobj.lch_h)) * float(cobj.lch_c)
   luvcolor.luv_v = math.sin(math.radians(cobj.lch_h)) * float(cobj.lch_c)
   return luvcolor

def XYZ_to_xyY(cobj):
   """
   Convert from XYZ to xyY.
   """
   xyycolor = color_objects.xyYColor()
   _transfer_common(cobj, xyycolor)
   
   xyycolor.xyy_x = (cobj.xyz_x) / (cobj.xyz_x + cobj.xyz_y + cobj.xyz_z)
   xyycolor.xyy_y = (cobj.xyz_y) / (cobj.xyz_x + cobj.xyz_y + cobj.xyz_z)
   xyycolor.xyy_Y = cobj.xyz_y
   
   return xyycolor

def XYZ_to_Luv(cobj):
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

def XYZ_to_Lab(cobj):
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

def XYZ_to_RGB(cobj, target_rgb="sRGB", debug=False):
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
   illum = cobj.get_illuminant_xyz()
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
      rgbcolor.rgb_r = math.pow(rgbcolor.rgb_r,(1 / gamma))
      rgbcolor.rgb_g = math.pow(rgbcolor.rgb_g,(1 / gamma))
      rgbcolor.rgb_b = math.pow(rgbcolor.rgb_b,(1 / gamma))

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

def xyY_to_XYZ(cobj):
   """
   Convert from xyY to XYZ.
   """
   xyzcolor = color_objects.XYZColor()
   _transfer_common(cobj, xyzcolor)
   
   xyzcolor.xyz_x = (cobj.xyy_x * cobj.xyy_Y) / (cobj.xyy_y)
   xyzcolor.xyz_y = cobj.xyy_Y
   xyzcolor.xyz_z = ((1.0 - cobj.xyy_x - cobj.xyy_y) * xyzcolor.xyz_y) / (cobj.xyy_y)
   return xyzcolor

def RGB_to_CMY(cobj, cdict):
   """
   RGB to CMY conversion.
   """
   cmycolor = color_objects.CMYColor()
   _transfer_common(cobj, cmycolor)
   
   cmycolor.cmy_c = 1 - (cobj.rgb_r / 255)
   cmycolor.cmy_m = 1 - (cobj.rgb_g / 255)
   cmycolor.cmy_y = 1 - (cobj.rgb_b / 255)
   return cmycolor

def RGB_to_XYZ(cobj, cdict):
   """
   Converts RGB to XYZ.
   """
   xyzcolor = color_objects.XYZColor()
   _transfer_common(cobj, xyzcolor)
   
   xyzcolor.xyz_x = 0.5
   xyzcolor.xyz_y = 0.5
   xyzcolor.xyz_z = 0.5
   return xyzcolor

def CMY_to_CMYK(cobj, cdict):
   """
   Converts from CMY to CMYK.
   
   NOTE: CMYK and CMY values range from 0 to 1
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
   return cmykcolor

import color_objects