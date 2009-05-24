#!/usr/bin/env python
"""
Imaged representation of an CIELab circle chart.
"""
#import time
import color_conversions
from PIL import Image, ImageDraw

SIZE = 300
OFFSET = 20
img = Image.new('RGB', (SIZE,SIZE), 'white')
draw = ImageDraw.Draw(img)

def pixel(coord):
    return coord + 128 + OFFSET

for a in range(-128, 128):
    #print a
    for b in range(-128, 128):
        color = color_conversions.Color()
        color.lab_l = 63.0
        color.lab_a = float(a)
        color.lab_b = float(b) * 1
        #print (color.lab_l,color.lab_a,color.lab_b)
        converted = color_conversions.cspace_conversion(color, cs_from="Lab", cs_to="LCH", obs_deg="2", illum="D50")
        #print img.size
        #print (newcol.lab_a, newcol.lab_b)
        #print (newcol.xyz_x, newcol.xyz_y, newcol.xyz_z)
        if abs(converted.lch_c) < 128:
            converted = color_conversions.cspace_conversion(converted, cs_from="Lab", cs_to="RGB", obs_deg="2", illum="D50", target_RGB="Adobe")
            x_c = pixel(converted.lab_a) 
            y_c = pixel(converted.lab_b * (-1))
            #print (x_c, y_c)
            #print (newcol.rgb_r, newcol.rgb_g, newcol.rgb_b)
            img.im.putpixel((x_c,y_c), (converted.rgb_r, converted.rgb_g, converted.rgb_b))
            #time.sleep(0.05)

# How much to subtract from the R, G, and B tri-stim values to make lines.
DARKENER = 10
# X axis lines
for y in range(0,SIZE,10):
    for x in range(0, SIZE):
        val = img.im.getpixel((x,y))
        if val != (255,255,255):
            img.im.putpixel((x,y),(val[0]-DARKENER,
                                   val[1]-DARKENER,
                                   val[2]-DARKENER))

# Y axis lines
for y in range(0,SIZE):
    for x in range(0,SIZE,10):
        val = img.im.getpixel((x,y))
        if val != (255,255,255):
            img.im.putpixel((x,y),(val[0]-DARKENER,
                                   val[1]-DARKENER,
                                   val[2]-DARKENER))
# Vertical Axis Line
begin = (SIZE/2, OFFSET+1)
end = (SIZE/2, SIZE-OFFSET-5)
draw.line((begin,end), width=1, fill='gray')
# Horizontal Axis Line
begin = (OFFSET+1, SIZE/2)
end = (SIZE-OFFSET-5, SIZE/2)
draw.line((begin,end), width=1, fill='gray')
            
draw.text((5,(SIZE/2)-5), "-a", fill='black')
draw.text((SIZE-20,(SIZE/2)-5), "+a", fill='black')
draw.text(((SIZE/2)-5, 9), "+b", fill='black')
draw.text(((SIZE/2)-5, SIZE-23), "-b", fill='black')
img.show()
