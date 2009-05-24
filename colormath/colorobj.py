class ColorObj(object):
   """
   Represents a color that may have operations done to it. You need not use
   this object with the library as long as you use all of the instance
   variables here.
   """
   def __init__(self):
       illuminant_key = "D50"
       observer_key = 2
       # Spectral fields
       spec_380nm = None # begin Blue wavelengths
       spec_390nm = None
       spec_400nm = None
       spec_410nm = None
       spec_420nm = None
       spec_430nm = None
       spec_440nm = None
       spec_450nm = None
       spec_460nm = None
       spec_470nm = None
       spec_480nm = None
       spec_490nm = None # end Blue wavelengths
       spec_500nm = None # start Green wavelengths
       spec_510nm = None
       spec_520nm = None
       spec_530nm = None
       spec_540nm = None
       spec_550nm = None
       spec_560nm = None
       spec_570nm = None
       spec_580nm = None
       spec_590nm = None
       spec_600nm = None
       spec_610nm = None # end Green wavelengths
       spec_620nm = None # start Red wavelengths
       spec_630nm = None
       spec_640nm = None
       spec_650nm = None
       spec_660nm = None
       spec_670nm = None
       spec_680nm = None
       spec_690nm = None
       spec_700nm = None
       spec_710nm = None
       spec_720nm = None
       spec_730nm = None # end Red wavelengths
       # CIELab values
       lab_l = None
       lab_a = None
       lab_b = None
       # Luv values
       luv_u = None
       luv_v = None
       # XYZ values
       xyz_x = None
       xyz_y = None
       xyz_z = None
       # xyY values
       xyy_x = None
       xyy_y = None
       # LCH values (Use L from lab_l)
       lch_c = None
       lch_h = None
       # RGB values (Cached for speed and ease of availability)
       rgb_r = None
       rgb_g = None
       rgb_b = None
       # CMYK values
       cmyk_c = None
       cmyk_m = None
       cmyk_y = None
       cmyk_k = None