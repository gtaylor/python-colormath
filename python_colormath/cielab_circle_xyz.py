"""
Imaged representation of an CIELab circle thing.
"""
import time
import color_conversions
from PIL import Image

img = Image.new('RGB', (101,101))

for x in range(0, 100):
    print x
    for y in range(0, 100):
        for z in range(0, 100):
            if x == 0 and y == 0 and z == 0:
                pass
            else:
                #print (x,y,z)
                color = color_conversions.Color()
                color.xyz_x = float(x) / 100.0
                color.xyz_y = y / 100.0
                color.xyz_z = z / 100.0
                #print "BLAH", (color.xyz_x, color.xyz_y, color.xyz_z)
                try:
                    converted = color_conversions.cspace_conversion(color, cs_from="XYZ", cs_to="xyY", obs_deg="2", illum="D50")
                    converted = color_conversions.cspace_conversion(converted, cs_from="XYZ", cs_to="RGB", obs_deg="2", illum="D50", target_RGB="sRGB")
                    #print img.size
                    #print (newcol.lab_a, newcol.lab_b)
                    #print (newcol.xyz_x, newcol.xyz_y, newcol.xyz_z)
                    x_c = converted.xyy_x * 10
                    y_c = converted.xyy_y * 10
                    #print (x_c, y_c)
                    #print (converted.rgb_r, converted.rgb_g, converted.rgb_b)
                    #print (newcol.rgb_r, newcol.rgb_g, newcol.rgb_b)
                    img.im.putpixel((x_c,y_c), (converted.rgb_r, converted.rgb_g, converted.rgb_b))
                    #time.sleep(0.05)
                    del converted
                except ZeroDivisionError:
                    pass
            
img.show()