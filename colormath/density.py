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
from colormath.density_standards import *

def ansi_density(color, std_array):
    """
    Calculates density for the given SpectralColor using the spectral weighting
    function provided. For example, ANSI_STATUS_T_RED. These may be found in
    density_standards.py.
    
    color: (SpectralColor) The SpectralColor object to calculate density for.
    std_array: (ndarray) NumPy array of filter of choice from density_standards.py.
    """  
    # Load the spec_XXXnm attributes into a Numpy array.
    sample = color.get_numpy_array()
    # Matrix multiplication
    intermediate = sample * std_array
    
    # Sum the products.
    numerator = intermediate.sum()
    # This is the denominator in the density equation.
    sum_of_standard_wavelengths = std_array.sum()
    
    # This is the top level of the density formula.
    return -1.0 * log10(numerator / sum_of_standard_wavelengths)

def auto_density(color):
    """
    Given a SpectralColor, automatically choose the correct ANSIT filter. Returns
    a tuple with a string representation of the filter the calculated density.
    """
    color_array = color.get_numpy_array()
    blue_density = ansi_density(color, ANSI_STATUS_T_BLUE)
    green_density = ansi_density(color, ANSI_STATUS_T_GREEN)
    red_density = ansi_density(color, ANSI_STATUS_T_RED)
    
    densities = [blue_density, green_density, red_density]
    min_density = min(densities)
    max_density = max(densities)
    density_range = max_density - min_density
    #print "DIFF", density_range
    
    # See comments in density_standards.py for VISUAL_DENSITY_THRESH to
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