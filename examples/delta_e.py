"""
This module shows some examples of Delta E calculations of varying types.
"""
import example_config
from colormath.color_objects import *

# Reference color.
color1 = LabColor(lab_l=0.9, lab_a=16.3, lab_b=-2.22)
# Color to be compared to the reference.
color2 = LabColor(lab_l=0.7, lab_a=14.2, lab_b=-1.80)

print "== Delta E Colors =="
print " COLOR1: %s" % color1
print " COLOR2: %s" % color2
print "== Results =="
print " CIE1976: %.3f" % color1.delta_e(color2, mode='cie1976')
print " CIE1994: %.3f (Graphic Arts)" % color1.delta_e(color2, mode='cie1994')
# Different values for textiles.
print " CIE1994: %.3f (Textiles)" % color1.delta_e(color2, mode='cie1994', 
                                                   K_1=0.048, K_2=0.014, 
                                                   K_L=2)
print " CIE2000: %.3f" % color1.delta_e(color2, mode='cie2000')
# Typically used for acceptability.
print "     CMC: %.3f (2:1)" % color1.delta_e(color2, mode='cmc', p1=2, pc=1)
# Typically used to more closely model human percetion.
print "     CMC: %.3f (1:1)" % color1.delta_e(color2, mode='cmc', p1=1, pc=1)