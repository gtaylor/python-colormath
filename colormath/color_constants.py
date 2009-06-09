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
Contains lookup tables, constants, and things that are generally static
and useful throughout the library.
"""
import numpy

# Not sure what these are, they are used in Lab and Luv calculations.
CIE_E = 216.0/24389.0
CIE_K = 24389.0/27.0

"""
This is a dictionary of RGB conversion matrices. These are applied to each
tri-stimulus values to convert between RGB and XYZ.
"""
RGB_SPECS = {
   # Adobe RGB (1998)
   "adobe_rgb": {
      "gamma": 2.2,
      "native_illum": "d65",
      "conversions": {
         "xyz_to_rgb":
            numpy.array((
                  ( 2.04148,    -0.969258,     0.0134455),  
                  (-0.564977,    1.87599,     -0.118373),   
                  (-0.344713,    0.0415557,    1.01527)
               )),
         "rgb_to_xyz":
            numpy.array((
                  ( 0.576700,    0.297361,    0.0270328),  
                  ( 0.185556,    0.627355,    0.0706879),   
                  ( 0.188212,    0.0752847,   0.991248)
               )),
      } # End Conversions Dict
   }, # End Adobe Dict
   # Apple RGB
   "apple_rgb": {
      "gamma": 1.8,
      "native_illum": "d65",
      "conversions": {
         "xyz_to_rgb":
            numpy.array((
                  ( 2.9515373,  -1.0851093,    0.0854934),  
                  (-1.2894116,   1.9908566,   -0.2694964),   
                  (-0.4738445,   0.0372026,    1.0912975)
               )),
         "rgb_to_xyz":
            numpy.array((
                  ( 0.4497288,   0.2446525,   0.0251848),  
                  ( 0.3162486,   0.6720283,   0.1411824),   
                  ( 0.1844926,   0.0833192,   0.9224628)
               )),
      } # End Conversions Dict
   }, # End Apple Dict
   # sRGB
   "srgb": {
      "gamma": 2.2,
      "native_illum": "d65",
      "conversions": {
         "xyz_to_rgb":
            numpy.array((
                  ( 3.24071,    -0.969258,    0.0556352),  
                  (-1.53726,     1.87599,    -0.203996),   
                  (-0.498571,    0.0415557,   1.05707 )
               )),
         "rgb_to_xyz":
            numpy.array((
                  ( 0.412424,    0.212656,    0.0193324),  
                  ( 0.357579,    0.715158,    0.119193),   
                  ( 0.180464,    0.0721856,   0.950444)
               )),
      } # End Conversions Dict
   }, # End sRGB Dict
   "wide_gamut_rgb": {
      "gamma": 2.2,
      "native_illum": "d50",
      "conversions": {
         "xyz_to_rgb":
            numpy.array((
                  ( 1.46281,    -0.521793,    0.0349342),  
                  (-0.184062,    1.44724,    -0.0968931),  
                  (-0.274361,    0.0677228,   1.28841)
               )),
         "rgb_to_xyz":
            numpy.array((
                  ( 0.716105,    0.258187,    0.000000),   
                  ( 0.100930,    0.724938,    0.0517813),  
                  ( 0.147186,    0.0168748,   0.773429)
               )),
      } # End Conversions Dict
   }, # End Wide Gamut RGB Dict
} # end RGB_SPECS Dict

# Observer Function and Illuminant Data
ILLUMINANTS = {
    # 2 Degree Functions
    '2': {
        'a': (1.09850, 1.00000, 0.35585),
        'b': (0.99072, 1.00000, 0.85223),
        'c': (0.98074, 1.00000, 1.18232),
        'd50': (0.96422, 1.00000, 0.82521),
        'd55': (0.95682, 1.00000, 0.92149),
        'd65': (0.95047, 1.00000, 1.08883),
        'd75': (0.94972, 1.00000, 1.22638),
        'e': (1.00000, 1.00000, 1.00000),
        'f2': (0.99186, 1.00000, 0.67393),
        'f7': (0.95041, 1.00000, 1.08747),
        'f11': (1.00962, 1.00000, 0.64350)
    },
    # 10 Degree Functions
    '10': {
        'd50': (0.9672,  1.000, 0.8143),
        'd55': (0.958,   1.000, 0.9093),
        'd65': (0.9481,  1.000, 1.073),
        'd75': (0.94416, 1.000, 1.2064),
    }
}

# Chromatic Adaptation Matrices
# http://brucelindbloom.com/Eqn_ChromAdapt.html
ADAPTATION_MATRICES = {
    'xyz_scaling': numpy.array(((1.0, 0.0, 0.0),     
                                (0.0, 1.0, 0.0),     
                                (0.0, 0.0, 1.0))),
    'bradford': numpy.array(((0.8951, -0.7502, 0.0389),  
                             (0.2664, 1.7135, -0.0685),  
                             (-0.1614, 0.0367, 1.0296))),
    'von_kries': numpy.array(((0.40024, -0.22630, 0.00000), 
                              (0.70760, 1.16532, 0.00000), 
                              (-0.08081, 0.04570, 0.91822)))
} # End ADAPTATION_MATRICES