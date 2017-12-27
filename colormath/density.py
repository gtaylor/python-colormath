"""
Formulas for density calculation.
"""

from math import log10
from colormath.density_standards import ANSI_STATUS_T_BLUE, ANSI_STATUS_T_GREEN, \
    ANSI_STATUS_T_RED, VISUAL_DENSITY_THRESH, ISO_VISUAL


def ansi_density(color, density_standard):
    """
    Calculates density for the given SpectralColor using the spectral weighting
    function provided. For example, ANSI_STATUS_T_RED. These may be found in
    :py:mod:`colormath.density_standards`.
    
    :param SpectralColor color: The SpectralColor object to calculate
        density for.
    :param numpy.ndarray std_array: NumPy array of filter of choice
        from :py:mod:`colormath.density_standards`.
    :rtype: float
    :returns: The density value for the given color and density standard.
    """
    # Load the spec_XXXnm attributes into a Numpy array.
    sample = color.get_numpy_array()
    # Matrix multiplication
    intermediate = sample * density_standard
    
    # Sum the products.
    numerator = intermediate.sum()
    # This is the denominator in the density equation.
    sum_of_standard_wavelengths = density_standard.sum()
    
    # This is the top level of the density formula.
    return -1.0 * log10(numerator / sum_of_standard_wavelengths)


def auto_density(color):
    """
    Given a SpectralColor, automatically choose the correct ANSI T filter.
    Returns a tuple with a string representation of the filter the
    calculated density.

    :param SpectralColor color: The SpectralColor object to calculate
        density for.
    :rtype: float
    :returns: The density value, with the filter selected automatically.
    """
    blue_density = ansi_density(color, ANSI_STATUS_T_BLUE)
    green_density = ansi_density(color, ANSI_STATUS_T_GREEN)
    red_density = ansi_density(color, ANSI_STATUS_T_RED)
    
    densities = [blue_density, green_density, red_density]
    min_density = min(densities)
    max_density = max(densities)
    density_range = max_density - min_density
    
    # See comments in density_standards.py for VISUAL_DENSITY_THRESH to
    # understand what this is doing.
    if density_range <= VISUAL_DENSITY_THRESH:
        return ansi_density(color, ISO_VISUAL)
    elif blue_density > green_density and blue_density > red_density:
        return blue_density
    elif green_density > blue_density and green_density > red_density:
        return green_density
    else:
        return red_density
