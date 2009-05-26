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
Various constants for density calculation.
"""
from numpy import array

# Visual density is typically used on grey patches. Take a reading and get
# the density values of the Red, Green, and Blue filters. If the difference
# between the highest and lowest value is less than or equal to the value
# below, return the density reading calculated against the ISO Visual spectral
# weighting curve. The X-Rite 500 uses a thresh of 0.05, the Gretag i1 appears
# to use 0.08.
VISUAL_DENSITY_THRESH = 0.08

# Log Base-10 ANSI StatusT
ANSIT_RED = array((
    10, # 380nm
    10,
    10,
    10,
    10,
    10,
    10,
    10,
    10,
    10,
    10,
    10,
    10,
    10,
    10,
    10,
    10,
    10,
    10,
    59.97910763, # 570nm
    449.7798549,
    29991.62519,
    100000,
    84918.0475,
    54954.08739,
    25003.45362,
    10000,
    5000.34535,
    1499.684836,
    500.034535,
    299.9162519,
    149.9684836,
    50.0034535, #700nm
    10,
    10,
    10 # 730nm
))

ANSIT_GREEN = array((
    10, # 380nm
    10,
    10,
    10,
    10,
    10,
    10,
    10,
    10,
    10,
    1000, # 480nm
    5000.34535,
    29991.62519, 
    68076.93587,
    92044.95718,
    100000,
    87902.25168,
    66069.3448,
    41975.8984,
    21978.59873,
    8994.975815,
    2500.345362,
    699.841996,
    89.94975815, # 610nm
    10,
    10,
    10,
    10,
    10,
    10,
    10,
    10,
    10,
    10,
    10,
    10, # 730nm
))

ANSIT_BLUE = array((
    299.9162519, # 380nm
    1499.684836,
    5997.910763,
    16982.43652,
    39994.47498,
    59979.10763,
    82035.15443,
    93972.33106,    
    100000,
    97050.99672,
    84918.0475,
    65012.96903,
    39994.47498,
    17988.70915,
    5000.34535,
    199.986187,
    39.99447498,
    10,
    10,
    10,
    10,
    10,
    10,
    10,
    10,
    10,
    10,
    10,
    10,
    10,
    10,
    10,
    10,
    10,
    10,
    10 # 730nm
))

ISO_VISUAL = array((
    1.000089805,
    1.000276348,
    1.00091224,
    1.002790013,
    1.009252886,
    1.027069896,
    1.054386896,
    1.091440336,
    1.148153621,
    1.233048048,
    1.377272893,
    1.614432902,
    2.10377844,
    3.184197522,
    5.12861384,
    7.277798045,
    8.994975815,
    9.884395174,
    9.885530947,
    8.953647655,
    7.413102413,
    5.714786367,
    4.275628862,
    3.184197522,
    2.4043628,
    1.840772001,
    1.496235656,
    1.279381304,
    1.150800389,
    1.076465214,
    1.039920166,
    1.01908404,
    1.009489951,
    1.004826315,
    1.002413715,
    1.001198061,
))