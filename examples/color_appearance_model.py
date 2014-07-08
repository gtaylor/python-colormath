from colormath.color_appearance_models import CIECAM02
from colormath.color_objects import XYZColor


# Color stimulus
color = XYZColor(19.01, 20, 21.78)

#Illuminant
illuminant_d65 = XYZColor(95.05, 100, 108.88)

# Background relative luminance
y_b_dark = 10
y_b_light = 100

# Adapting luminance
l_a = 328.31

# Surround condition assumed to be average (see CIECAM02 documentation for values)
c = 0.69
n_c = 1
f = 1

model_a = CIECAM02(color.xyz_x, color.xyz_y, color.xyz_z,
                   illuminant_d65.xyz_x, illuminant_d65.xyz_y, illuminant_d65.xyz_z,
                   y_b_dark, l_a, c, n_c, f)
model_b = CIECAM02(color.xyz_x, color.xyz_y, color.xyz_z,
                   illuminant_d65.xyz_x, illuminant_d65.xyz_y, illuminant_d65.xyz_z,
                   y_b_light, l_a, c, n_c, f)

print('== CIECAM02 Predictions ==')

print('Observed under CIE illuminant D65')
print('Lightness {:.2f}, saturation {:.2f}, hue {:.2f}'.format(model_a.lightness, model_a.saturation, model_a.hue_angle))
print('Observed under CIE illuminant A')
print('Lightness {:.2f}, saturation {:.2f}, hue {:.2f}'.format(model_b.lightness, model_b.saturation, model_b.hue_angle))


