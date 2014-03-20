"""
This module shows some examples of Delta E calculations of varying types.
"""

# Does some sys.path manipulation so we can run examples in-place.
# noinspection PyUnresolvedReferences
import example_config

from colormath.color_objects import LabColor
from colormath.color_diff import delta_e_cie1976, delta_e_cie1994, \
    delta_e_cie2000, delta_e_cmc

# Reference color.
color1 = LabColor(lab_l=0.9, lab_a=16.3, lab_b=-2.22)
# Color to be compared to the reference.
color2 = LabColor(lab_l=0.7, lab_a=14.2, lab_b=-1.80)

print("== Delta E Colors ==")
print(" COLOR1: %s" % color1)
print(" COLOR2: %s" % color2)
print("== Results ==")
print(" CIE1976: %.3f" % delta_e_cie1976(color1, color2))
print(" CIE1994: %.3f (Graphic Arts)" % delta_e_cie1994(color1, color2))
# Different values for textiles.
print(" CIE1994: %.3f (Textiles)" % delta_e_cie1994(color1,
    color2, K_1=0.048, K_2=0.014, K_L=2))
print(" CIE2000: %.3f" % delta_e_cie2000(color1, color2))
# Typically used for acceptability.
print("     CMC: %.3f (2:1)" % delta_e_cmc(color1, color2, pl=2, pc=1))
# Typically used to more closely model human perception.
print("     CMC: %.3f (1:1)" % delta_e_cmc(color1, color2, pl=1, pc=1))
