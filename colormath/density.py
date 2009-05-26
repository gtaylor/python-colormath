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
Formulas for density calculation.
"""
from math import log10, log
from colormath.color_objects import SpectralColor
from colormath.density_constants import *

def ansi_density(color, std_array):
    """
    calculates density for the given color using the spectral weighting
    function provided. For example, ANSIT_RED. These may be found in
    density_constants.py.
    
    color: (Color) The Color object to calculate density for.
    std_array: (ndarray) NumPy array of filter of choice from density_constants.py.
    """  
    # Load the spec_XXXnm attributes into a Numpy array.
    color_array = util_functions.color_to_numpy_array(color)
    # Matrix multiplication
    intermediate = color_array * std_array
    
    # Sum the products.
    numerator = intermediate.sum()
    sum_of_standard_wavelengths = std_array.sum()
    
    return -1 * log10(numerator / sum_of_standard_wavelengths)

def auto_density(color):
    """
    Given a color, automatically choose the correct ANSIT filter. Returns
    a tuple with a string representation of the filter the calculated density.
    """
    color_array = util_functions.color_to_numpy_array(color)
    blue_density = ansi_density(color, ANSIT_BLUE)
    green_density = ansi_density(color, ANSIT_GREEN)
    red_density = ansi_density(color, ANSIT_RED)
    
    densities = [blue_density, green_density, red_density]
    min_density = min(densities)
    max_density = max(densities)
    density_range = max_density - min_density
    #print "DIFF", density_range
    
    # See comments in density_constants.py for VISUAL_DENSITY_THRESH to
    # understand what this is doing.
    if density_range <= VISUAL_DENSITY_THRESH:
        #print "visual"
        return ansi_density(color, ISO_VISUAL)
    elif blue_density > green_density and blue_density > red_density:
        #print "blue"
        return blue_density
    elif green_density > blue_density and green_density > red_density:
        #print "green"
        return green_density
    else:
        #print "red"
        return red_density
        
if __name__ == "__main__":
    """
    Console testing stuff.
    """
    test = Color()
    print auto_density(test)