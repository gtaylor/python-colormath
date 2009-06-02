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
   "2": {
      "d50": {"X": 96.42,  "Y": 100.0, "Z": 82.52},
      "d55": {"X": 95.68,  "Y": 100.0, "Z": 92.15},
      "d65": {"X": 95.05,  "Y": 100.0, "Z": 108.88},
      "d75": {"X": 94.97,  "Y": 100.0, "Z": 122.64},
   },
   # 10 Degree Functions
   "10": {
      "d50": {"X": 96.72,  "Y": 100.0, "Z": 81.43},
      "d55": {"X": 95.8,   "Y": 100.0, "Z": 90.93},
      "d65": {"X": 94.81,  "Y": 100.0, "Z": 107.3},
      "d75": {"X": 94.416, "Y": 100.0, "Z": 120.64},
   }
}

# Chromatic Adaptation Matrices
# http://brucelindbloom.com/Eqn_ChromAdapt.html
ADAPTATION_MATRICES = {
   "d50": {
      "d55": {
         "bradford":
            numpy.array((
               ( 0.981751, -0.012159,  0.004411),
               (-0.009617,  1.005251, -0.007265),
               ( 0.023309,  0.007844,  1.119548)
            ))
      },
      "d65": {
         "bradford":
            numpy.array((
               ( 0.955556, -0.028302,  0.012305),
               (-0.023049,  1.009944, -0.020494),
               ( 0.063197,  0.021018,  1.330084)
            ))
      },
      "d75": {
         "bradford":
            numpy.array((
               ( 0.936847, -0.039129,  0.018781),
               (-0.032442,  1.011771, -0.031445),
               ( 0.095135,  0.031456,  1.501335)
            ))
      },
   }, # End D50 Conversions
   "d55": {
      "d50": {
         "bradford":
            numpy.array((
               ( 1.018803,  0.012353, -0.003934),
               ( 0.009594,  0.994842,  0.006418),
               (-0.021278, -0.007227,  0.893255)
            ))
      },
      "d65": {
         "bradford":
            numpy.array((
               ( 0.972990, -0.016440,  0.007051),
               (-0.013357,  1.004598, -0.011734),
               ( 0.036285,  0.012078,  1.187991)
            ))
      },
      "d75": {
         "bradford":
            numpy.array((
               ( 0.953688, -0.027490,  0.012840),
               (-0.022677,  1.006379, -0.021468),
               ( 0.065280,  0.021618,  1.340903)
            ))
      },
   }, # End D55 Conversions
   "d65": {
      "d50": {
         "bradford":
            numpy.array((
               ( 1.047835,  0.029556, -0.009238),
               ( 0.022897,  0.990481,  0.015050),
               (-0.050147, -0.017056,  0.752034)
            ))
      },
      "d55": {
         "bradford":
            numpy.array((
               ( 1.028213,  0.016898, -0.005936),
               ( 0.013304,  0.995522,  0.009754),
               (-0.031540, -0.010637,  0.841840)
            ))
      },
      "d75": {
         "bradford":
            numpy.array((
               ( 0.979823, -0.011388,  0.004880),
               (-0.009251,  1.001719, -0.008121),
               ( 0.025117,  0.008361,  1.128649)
            ))
      },
   }, # End D65 Conversions
   "d75": {
      "d50": {
         "bradford":
            numpy.array((
               ( 1.070127,  0.041775, -0.012512),
               ( 0.032186,  0.988978,  0.020311),
               (-0.068484, -0.023368,  0.666442)
            ))
      },
      "d55": {
         "bradford":
            numpy.array((
               ( 1.049904,  0.028885, -0.009591),
               ( 0.022560,  0.993940,  0.015697),
               (-0.051476, -0.017431,  0.745981)
            ))
      },
      "d65": {
         "bradford":
            numpy.array((
               ( 1.020813,  0.011641, -0.004330),
               ( 0.009243,  0.998329,  0.007144),
               (-0.022785, -0.007655,  0.886059)
            ))
      },
   }, # End D75 Conversions
} # End ADAPTATION_MATRICES

SPECDIST_2_D50_X = numpy.array((
   0.003, # 380nm
   0.012,
   0.060,
   0.234,
   0.775,
   1.610,
   2.453,
   2.777,
   2.500,
   1.717,
   0.861,
   0.283,
   0.040,
   0.088,
   0.593,
   1.590,
   2.799,
   4.207,
   5.657,
   7.132,
   8.540,
   9.255,
   9.835,
   9.469,
   8.009,
   5.926,
   4.171,
   2.609,
   1.541,
   0.855,
   0.434,
   0.194,
   0.097,
   0.050,
   0.022,
   0.012  # 730nm
))

SPECDIST_2_D50_Y = numpy.array((
   0.000,
   0.000,
   0.002,
   0.006,
   0.023,
   0.066,
   0.162,
   0.313,
   0.514,
   0.798,
   1.239,
   1.839,
   2.948,
   4.632,
   6.587,
   8.308,
   9.197,
   9.650,
   9.471,
   8.902,
   8.112,
   6.829,
   5.838,
   4.753,
   3.573,
   2.443,
   1.629,
   0.984,
   0.570,
   0.313,
   0.158,
   0.070,
   0.035,
   0.018,
   0.008,
   0.004
))

SPECDIST_2_D50_Z = numpy.array((
   0.013,
   0.057,
   0.285,
   1.113,
   3.723,
   7.862,
  12.309,
  14.647,
  14.346,
  11.299,
   7.309,
   4.128,
   2.466,
   1.447,
   0.736,
   0.401,
   0.196,
   0.085,
   0.037,
   0.020,
   0.015,
   0.010,
   0.007,
   0.004,
   0.002,
   0.001,
   0.000,
   0.000,
   0.000,
   0.000,
   0.000,
   0.000,
   0.000,
   0.000,
   0.000,
   0.000
))

# Spectral Power Distributions
SPECTRAL_DISTS = {
   # 2 Degree Functions
   "2": {
      "d50": {"X": SPECDIST_2_D50_X,  "Y": SPECDIST_2_D50_Y, "Z": SPECDIST_2_D50_Z},
   },
   # 10 Degree Functions
   "10": {
      "d65": {"X": SPECDIST_2_D50_X,  "Y": SPECDIST_2_D50_Y, "Z": SPECDIST_2_D50_Z},
   }
}
