"""
Conversion between color spaces
"""
import math
import numpy
import constants
import util_functions
from color_exceptions import MissingValue

def apply_XYZ_transformation(cobj, orig_illum, targ_illum, adaptation="Bradford"):
   """
   Applies an XYZ transformation matrix to convert XYZ values between
   illuminants. It is important to recognize that color transformation results
   in color errors, determined by how far the original illuminant is from the
   target illuminant. For example, D65 to A could result in very high maximum
   deviances. 
   """
   # Retrieve the appropriate transformation matrix from the constants.
   transform_matrix = constants.ADAPTATION_MATRICES[orig_illum][targ_illum][adaptation]
   if None in [cobj.xyz_x, cobj.xyz_y, cobj.xyz_z]:
       raise MissingValue("XYZ values missing.")
   # Stuff the XYZ values into a NumPy matrix for conversion.
   XYZ_matrix = numpy.array((
      cobj.xyz_x, cobj.xyz_y, cobj.xyz_z
   ))
   # Perform the adaptation via matrix multiplication.
   result_matrix = numpy.dot(XYZ_matrix, transform_matrix)
   # Return the results
   return result_matrix[0], result_matrix[1], result_matrix[2]

def apply_RGB_matrix(var1, var2, var3, RGB_type, convtype="XYZ_to_RGB"):
   """
   Applies an RGB working matrix to convert from XYZ to RGB.
   The arguments are tersely named var1, var2, and var3 to allow for the passing
   of XYZ _or_ RGB values. var1 is X for XYZ, and R for RGB. var2 and var3
   follow suite.
   """
   # Retrieve the appropriate transformation matrix from the constants.
   rgb_matrix = constants.RGB_SPECS[RGB_type]["conversions"][convtype]
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
   illuminants = constants.SPECTRAL_DISTS[cdict["observer"]][cdict["illum_str"]]
   sample = util_functions.color_to_numpy_array(cobj)
   cobj.xyz_x = float(numpy.dot(sample, illuminants["X"]) / 100)
   cobj.xyz_y = float(numpy.dot(sample, illuminants["Y"]) / 100)
   cobj.xyz_z = float(numpy.dot(sample, illuminants["Z"]) / 100)
   return cobj

def Lab_to_LCH(cobj, cdict):
   """
   Convert from CIE Lab to LCH(ab).
   """
   cobj.lch_c = math.sqrt(math.pow(float(cobj.lab_a),2) + math.pow(float(cobj.lab_b),2))
   cobj.lch_h = math.atan2(float(cobj.lab_b), float(cobj.lab_a))
   
   if (cobj.lch_h > 0):
      cobj.lch_h = (cobj.lch_h / math.pi) * 180
   else:
      cobj.lch_h = 360 - (math.fabs(cobj.lch_h) / math.pi) * 180
   return cobj

def Lab_to_XYZ(cobj, cdict):
   """
   Convert from Lab to XYZ
   """
   illum = cdict["illum"]
   
   cobj.xyz_y = (cobj.lab_l + 16.0) / 116.0
   cobj.xyz_x = cobj.lab_a / 500.0 + cobj.xyz_y
   cobj.xyz_z = cobj.xyz_y - cobj.lab_b / 200.0
   
   if math.pow(cobj.xyz_y, 3) > 0.008856:
      cobj.xyz_y = math.pow(cobj.xyz_y, 3)
   else:
      cobj.xyz_y = (cobj.xyz_y - 16.0 / 116.0) / 7.787

   if math.pow(cobj.xyz_x, 3) > 0.008856:
      cobj.xyz_x = math.pow(cobj.xyz_x, 3)
   else:
      cobj.xyz_x = (cobj.xyz_x - 16.0 / 116.0) / 7.787
      
   if math.pow(cobj.xyz_z, 3) > 0.008856:
      cobj.xyz_z = math.pow(cobj.xyz_z, 3)
   else:
      cobj.xyz_z = (cobj.xyz_z - 16.0 / 116.0) / 7.787
      
   # Adjust via illuminant and scale down to 0-1 values.
   cobj.xyz_x = (illum["X"] * cobj.xyz_x) / 100
   cobj.xyz_y = (illum["Y"] * cobj.xyz_y) / 100
   cobj.xyz_z = (illum["Z"] * cobj.xyz_z) / 100
   return cobj

def Luv_to_LCH(cobj, cdict):
   """
   Convert from CIE Luv to LCH(uv).
   """
   cobj.lch_c = math.sqrt(math.pow(float(cobj.luv_u), 2) + math.pow(float(cobj.luv_v), 2))
   cobj.lch_h = math.atan2(float(cobj.luv_v), float(cobj.luv_u))
   
   if (cobj.lch_h > 0):
      cobj.lch_h = (cobj.lch_h / math.pi) * 180
   else:
      cobj.lch_h = 360 - (math.fabs(cobj.lch_h) / math.pi) * 180
   return cobj

def Luv_to_XYZ(cobj, cdict):
   """
   Convert from Luv to XYZ.
   illum["X"]
   """
   illum  = cdict["illum"]
   
   ref_U = ( 4.0 * illum["X"] ) / ( illum["X"] + ( 15.0 * illum["Y"] ) + ( 3.0 * illum["Z"] ) )
   ref_V = ( 9.0 * illum["Y"] ) / ( illum["X"] + ( 15.0 * illum["Y"] ) + ( 3.0 * illum["Z"] ) )
   var_U = cobj.luv_u / ( 13.0 * cobj.lab_l ) + ref_U
   var_V = cobj.luv_u / ( 13.0 * cobj.lab_l ) + ref_V
   var_Y = ( cobj.lab_l + 16 ) / 116.0

   if math.pow(var_Y, 3) > 0.008856: 
      var_Y = math.pow(var_Y, 3)
   else:
      var_Y = ( var_Y - 16.0 / 116.0 ) / 7.787

   cobj.xyz_y = var_Y * 100.0
   cobj.xyz_x =  - ( 9.0 * cobj.xyz_y * var_U ) / ( ( var_U - 4.0 ) * var_V  - var_U * var_V )
   cobj.xyz_z = ( 9.0 * cobj.xyz_y - ( 15.0 * var_V * cobj.xyz_y ) - ( var_V * cobj.xyz_x ) ) / ( 3.0 * var_V )
   return cobj

def LCH_to_Lab(cobj, cdict):
   """
   Convert from LCH(ab) to Lab.
   """
   new_a = math.cos(math.radians(float(cobj.lch_h))) * float(cobj.lch_c)
   new_b = math.sin(math.radians(float(cobj.lch_h))) * float(cobj.lch_c)
   return cobj

def LCH_to_Luv(cobj, cdict):
   """
   Convert from LCH(ab) to Luv.
   """
   new_u = math.cos(math.radians(float(cobj.lch_h))) * float(cobj.lch_c)
   new_v = math.sin(math.radians(float(cobj.lch_h))) * float(cobj.lch_c)
   return cobj

def XYZ_to_xyY(cobj, cdict):
   """
   Convert from XYZ to xyY.
   """
   cobj.xyy_x = (cobj.xyz_x) / (cobj.xyz_x + cobj.xyz_y + cobj.xyz_z)
   cobj.xyy_y = (cobj.xyz_y) / (cobj.xyz_x + cobj.xyz_y + cobj.xyz_z)
   return cobj

def XYZ_to_Luv(cobj, cdict):
   """
   Convert from XYZ to Luv
   """
   cobj.xyz_x = cobj.xyz_x * 100
   cobj.xyz_y = cobj.xyz_y * 100
   cobj.xyz_z = cobj.xyz_z * 100
   illum  = cdict["illum"]
   
   cobj.luv_u = (4.0 * cobj.xyz_x) / (cobj.xyz_x + (15 * cobj.xyz_y) + (3 * cobj.xyz_z))
   cobj.luv_v = (9.0 * cobj.xyz_y) / (cobj.xyz_x + (15 * cobj.xyz_y) + (3 * cobj.xyz_z))
   
   cobj.xyz_y = float(cobj.xyz_y) / illum["Y"]
   if cobj.xyz_y > 0.008856:
      cobj.xyz_y = math.pow(cobj.xyz_y, (1.0 / 3.0))
   else:
      cobj.xyz_y = (7.787 * cobj.xyz_y) + (16.0 / 116.0)
   
   ref_U = (4 * illum["X"]) / (illum["X"] + (15 * illum["Y"]) + (3 * illum["Z"]))
   ref_V = (9 * illum["Y"]) / (illum["X"] + (15 * illum["Y"]) + (3 * illum["Z"]))
   
   cobj.lab_l = (116.0 * cobj.xyz_y) - 16
   cobj.luv_u = 13.0 * cobj.lab_l * (cobj.luv_u - ref_U)
   cobj.luv_v = 13.0 * cobj.lab_l * (cobj.luv_v - ref_V)
   return cobj

def XYZ_to_Lab(cobj, cdict):
   """
   Converts XYZ to Lab.
   """
   temp_x = (cobj.xyz_x * 100.0) / cdict["illum"]["X"]
   temp_y = (cobj.xyz_y * 100.0) / cdict["illum"]["Y"]
   temp_z = (cobj.xyz_z * 100.0) / cdict["illum"]["Z"]
   
   if temp_x > 0.008856:
      temp_x = math.pow(temp_x, (1.0 / 3.0))
   else:
      temp_x = (7.787 * temp_x) + (16.0 / 116.0)     

   if temp_y > 0.008856:
      temp_y = math.pow(temp_y, (1.0 / 3.0))
   else:
      temp_y = (7.787 * temp_y) + (16.0 / 116.0)
   
   if temp_z > 0.008856:
      temp_z = math.pow(temp_z, (1.0 / 3.0))
   else:
      temp_z = (7.787 * temp_z) + (16.0 / 116.0)
      
   cobj.lab_l = (116.0 * temp_y) - 16.0
   cobj.lab_a = 500.0 * (temp_x - temp_y)
   cobj.lab_b = 200.0 * (temp_y - temp_z)
   return cobj

def XYZ_to_RGB(cobj, cdict):
   """
   XYZ to RGB conversion.
   """
   target_RGB = cdict["target_RGB"]
   target_illum = constants.RGB_SPECS[target_RGB]["native_illum"]
   
   # If the XYZ values were taken with a different reference white than the
   # native reference white of the target RGB space, a transformation matrix
   # must be applied.
   if cdict["illum_str"] != target_illum:
      if cdict["debug"]:
         print "Applying transformation from", cdict["illum_str"], "to", target_illum
      temp_X = cobj.xyz_x
      temp_Y = cobj.xyz_y
      temp_Z = cobj.xyz_z
      temp_X, temp_Y, temp_Z = apply_XYZ_transformation(cobj, 
         orig_illum=cdict["illum_str"], targ_illum=target_illum)
   
   # Apply an RGB working space matrix to the XYZ values (matrix mul).
   cobj.rgb_r, cobj.rgb_g, cobj.rgb_b = apply_RGB_matrix(temp_X, 
                                          temp_Y, 
                                          temp_Z, 
                                          RGB_type=target_RGB, 
                                          convtype="XYZ_to_RGB")

   if target_RGB == "sRGB":
      # If it's sRGB...
      if cobj.rgb_r > 0.0031308:
         cobj.rgb_r = (1.055 * math.pow(cobj.rgb_r, 1.0 / 2.4)) - 0.055
      else:
         cobj.rgb_r = cobj.rgb_r * 12.92
   
      if cobj.rgb_g > 0.0031308:
         cobj.rgb_g = (1.055 * math.pow(cobj.rgb_g, 1.0 / 2.4)) - 0.055
      else:
         cobj.rgb_g = cobj.rgb_g * 12.92
   
      if cobj.rgb_b > 0.0031308:
         cobj.rgb_b = (1.055 * math.pow(cobj.rgb_b, 1.0 / 2.4)) - 0.055
      else:
         cobj.rgb_b = cobj.rgb_b * 12.92
   else:
      # If it's not sRGB...
      gamma = constants.RGB_SPECS[target_RGB]["gamma"]
      
      if cobj.rgb_r < 0:
         cobj.rgb_r = 0
      if cobj.rgb_g < 0:
         cobj.rgb_g = 0
      if cobj.rgb_b < 0:
         cobj.rgb_b = 0
      
      #print "RGB", cobj.rgb_r, cobj.rgb_g, cobj.rgb_b
      cobj.rgb_r = math.pow(cobj.rgb_r,(1 / gamma))
      cobj.rgb_g = math.pow(cobj.rgb_g,(1 / gamma))
      cobj.rgb_b = math.pow(cobj.rgb_b,(1 / gamma))

   # RGB values are to not go under 0.
   if cobj.rgb_r < 0:
      cobj.rgb_r = 0
   if cobj.rgb_g < 0:
      cobj.rgb_g = 0
   if cobj.rgb_b < 0:
      cobj.rgb_b = 0
      
   # Scale up to 0-255 values.
   cobj.rgb_r = int(math.floor(0.5 + cobj.rgb_r * 255))
   cobj.rgb_g = int(math.floor(0.5 + cobj.rgb_g * 255))
   cobj.rgb_b = int(math.floor(0.5 + cobj.rgb_b * 255))

   # Cap RGB values at 255. This shouldn't happen, but it's here just in case
   # things go out of gamut or other fun things.
   if cobj.rgb_r > 255:
      cobj.rgb_r = 255
   if cobj.rgb_g > 255:
      cobj.rgb_g = 255
   if cobj.rgb_b > 255:
      cobj.rgb_b = 255
   return cobj

def xyY_to_XYZ(cobj, cdict):
   """
   Convert from xyY to XYZ.
   """
   cobj.xyz_x = (cobj.xyy_x * cobj.xyz_y) / (cobj.xyy_y)
   cobj.xyz_z = ((1.0 - cobj.xyy_x - cobj.xyy_y) * cobj.xyz_y) / (cobj.xyy_y)
   return cobj

def RGB_to_CMY(cobj, cdict):
   """
   RGB to CMY conversion.
   """
   cobj.cmyk_c = 1 - (cobj.rgb_r / 255)
   cobj.cmyk_m = 1 - (cobj.rgb_g / 255)
   cobj.cmyk_y = 1 - (cobj.rgb_b / 255)
   return cobj

def RGB_to_XYZ(cobj, cdict):
   """
   Converts RGB to XYZ.
   """
   cobj.xyz_x = 5
   cobj.xyz_y = 5
   cobj.xyz_z = 5
   return cobj

def CMY_to_CMYK(cobj, cdict):
   """
   Converts from CMY to CMYK.
   
   NOTE: CMYK and CMY values range from 0 to 1
   """ 
   cobj.cmyk_k = 1
   if cobj.cmyk_c < cobj.cmyk_k:
      cobj.cmyk_k = cobj.cmyk_c
   if cobj.cmyk_m < cobj.cmyk_k:
      cobj.cmyk_k = cobj.cmyk_m
   if cobj.cmyk_y < cobj.cmyk_k:
      cobj.cmyk_k = cobj.cmyk_y
      
   if cobj.cmyk_k == 1:
      cobj.cmyk_c = 0
      cobj.cmyk_m = 0
      cobj.cmyk_y = 0
   else:
      cobj.cmyk_c = (cobj.cmyk_c - cobj.cmyk_k) / (1 - cobj.cmyk_k)
      cobj.cmyk_m = (cobj.cmyk_m - cobj.cmyk_k) / (1 - cobj.cmyk_k)
      cobj.cmyk_y = (cobj.cmyk_y - cobj.cmyk_k) / (1 - cobj.cmyk_k)
   return cobj

# Table that handles converting between colorspaces.
CSPACE_CONV_TABLE = {
   "Spectral": {
         "XYZ": [Spectral_to_XYZ],
         "xyY": [Spectral_to_XYZ, XYZ_to_xyY],
         "Lab": [Spectral_to_XYZ, XYZ_to_Lab],
         "LCH": [Spectral_to_XYZ, XYZ_to_Lab, Lab_to_LCH],
         "Luv": [Spectral_to_XYZ, XYZ_to_Luv],
         "RGB": [Spectral_to_XYZ, XYZ_to_RGB],
   },
   "XYZ": {
         "xyY": [XYZ_to_xyY],
         "Lab": [XYZ_to_Lab],
         "LCH": [XYZ_to_Lab, Lab_to_LCH],
         "Luv": [XYZ_to_Luv],
         "RGB": [XYZ_to_RGB],
   },
   "xyY": {
         "XYZ": [xyY_to_XYZ],
         "Lab": [xyY_to_XYZ, XYZ_to_Lab],
         "LCH": [xyY_to_XYZ, XYZ_to_Lab, Lab_to_LCH],
         "Luv": [xyY_to_XYZ, XYZ_to_Luv],
         "RGB": [xyY_to_XYZ, XYZ_to_RGB],
   },
   "Lab": {
         "XYZ": [Lab_to_XYZ],
         "xyY": [Lab_to_XYZ, XYZ_to_xyY],
         "LCH": [Lab_to_LCH],
         "Luv": [Lab_to_XYZ, XYZ_to_Luv],
         "RGB": [Lab_to_XYZ, XYZ_to_RGB],
   },
   "LCH": {
         "XYZ": [LCH_to_Lab, Lab_to_XYZ],
         "xyY": [LCH_to_Lab, Lab_to_XYZ, XYZ_to_xyY],
         "Lab": [LCH_to_Lab],
         "Luv": [LCH_to_Lab, Lab_to_XYZ, XYZ_to_Luv],
         "RGB": [LCH_to_Lab, Lab_to_XYZ, XYZ_to_RGB],
   },
   "Luv": {
         "XYZ": [Luv_to_XYZ],
         "xyY": [Luv_to_XYZ, XYZ_to_xyY],
         "Lab": [Luv_to_XYZ, XYZ_to_Lab],
         "LCH": [Luv_to_XYZ, XYZ_to_Lab, Lab_to_LCH],
         "RGB": [Luv_to_XYZ, XYZ_to_RGB],
   },
   "RGB": {
         "XYZ": [RGB_to_XYZ],
         "xyY": [RGB_to_XYZ, XYZ_to_xyY],
         "Lab": [RGB_to_XYZ, XYZ_to_Lab],
         "LCH": [RGB_to_XYZ, XYZ_to_Lab, Lab_to_LCH],
         "Luv": [RGB_to_XYZ, XYZ_to_RGB],
   }
}

def cspace_conversion(cobj, cs_from, cs_to, obs_deg="2", illum="D50", target_RGB="sRGB", debug=False):
   """
   This function ties pretty much everything above together. The user builds
   a dictionary of values for their current color, (keys being things like X, Y,
   Z, or L, a, b) and populates the cs_from and cs_to variables to choose the
   conversion path.
   
   cobj (Color or Color_Reading): Color or Color_Reading object to convert.
   cs_from (string): Name of the original colorspace
   cs_to (string): Name of the destination colorspace
   obs_deg (string): The observer degree function: 2 or 10
   illum (string): Reference illuminant
   target_RGB (string): The name of the RGB space to convert to (XYZ->RGB).
   debug (boolean): If true, verbose debugging info is output.
   """
   # Dictionary of configuration for the conversion.
   cdict = {}
   cdict["debug"] = debug
   cdict["target_RGB"] = target_RGB
   cdict["illum"] = constants.ILLUMINANTS[str(obs_deg)][str(illum)]
   cdict["illum_str"] = str(illum)
   cdict["observer"]  = str(obs_deg)
   
   # Load up the conversion function path based on input.
   conv_funcs = CSPACE_CONV_TABLE[cs_from][cs_to]
   # Iterate through the list of functions for the conversion path, storing
   # the results in a dictionary via update(). This way the user has access
   # to all of the variables involved in the conversion.
   for func in conv_funcs:
      # Execute the function in this conversion step and store the resulting
      # Color object.
      new_cobj = func(cobj, cdict)
      
   # Verbose debugging output.
   if debug:
      print "--[Summary]----------"
      print "From:", cs_from, " To:", cs_to
      print "Illum:", obs_deg, "degree", illum
      print "--[XYZ]--------------"
      print "X:", cobj.xyz_x
      print "Y:", cobj.xyz_y
      print "Z:", cobj.xyz_z
      print "--[xyY]--------------"
      print "x:", cobj.xyy_x
      print "y:", cobj.xyy_y
      print "Y:", cobj.xyz_y
      print "--[Lab]--------------"
      print "L:", cobj.lab_l
      print "a:", cobj.lab_a
      print "b:", cobj.lab_b
      print "--[LCH]--------------"
      print "L:", cobj.lab_l
      print "C:", cobj.lch_c
      print "H:", cobj.lch_h
      print "--[Luv]--------------"
      print "L:", cobj.lab_l
      print "u:", cobj.luv_u
      print "v:", cobj.luv_v
      print "--[RGB]--------------"
      print "R:", cobj.rgb_r
      print "G:", cobj.rgb_g
      print "B:", cobj.rgb_b
   # Return the new Color Object for the user to access directly.
   return cobj

if __name__ == "__main__":
    """
    Console testing stuff.
    """
    test = Color()
    test.xyz_x = 0.5
    test.xyz_y = 0.5
    test.xyz_z = 0.5
    
    converted = cspace_conversion(test, cs_from="Spectral", cs_to="RGB", obs_deg="2", illum="D50", target_RGB="Adobe", debug=True)
    #converted = cspace_conversion(test, cs_from="XYZ", cs_to="RGB", obs_deg="2", illum="D50", target_RGB="Adobe", debug=True)
    #converted = cspace_conversion(converted, cs_from="LCH", cs_to="Lab", obs_deg="2", illum="D50")
    #converted = cspace_conversion(converted, cs_from="XYZ", cs_to="RGB", obs_deg="2", illum="D50", target_RGB="sRGB", debug=True)
    

    
    #converted = cspace_conversion(test, cs_from="Lab", cs_to="LCH", obs_deg="2", illum="D50", debug=True)
    #converted = cspace_conversion(converted, cs_from="XYZ", cs_to="LCH", obs_deg="2", illum="D50", debug=False)
    #converted = cspace_conversion(converted, cs_from="XYZ", cs_to="Luv", obs_deg="2", illum="D50", debug=True)
    #cdict = cspace_conversion(cdict, cs_from="XYZ", cs_to="LCH", obs_deg="2", illum="D50")
    #cdict = cspace_conversion(cdict, cs_from="XYZ", cs_to="Luv", obs_deg="2", illum="D50")
    #cdict = cspace_conversion(cdict, cs_from="XYZ", cs_to="xyY", obs_deg="2", illum="D50")
    #cdict = cspace_conversion(cdict, cs_from="XYZ", cs_to="RGB", obs_deg="2", illum="D50", debug=True)
    #cdict = cspace_conversion(cdict, cs_from="XYZ", cs_to="Lab", obs_deg="2", illum="D50", debug=True)
    #cspace_conversion(cdict, cs_from="Lab", cs_to="RGB", obs_deg="2", illum="D50", debug=True)

