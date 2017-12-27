import logging

import numpy
from numpy.linalg import pinv

from colormath import color_constants

logger = logging.getLogger(__name__)


# noinspection PyPep8Naming
def _get_adaptation_matrix(wp_src, wp_dst, observer, adaptation):
    """
    Calculate the correct transformation matrix based on origin and target
    illuminants. The observer angle must be the same between illuminants.

    See colormath.color_constants.ADAPTATION_MATRICES for a list of possible
    adaptations.

    Detailed conversion documentation is available at:
    http://brucelindbloom.com/Eqn_ChromAdapt.html
    """
    # Get the appropriate transformation matrix, [MsubA].
    m_sharp = color_constants.ADAPTATION_MATRICES[adaptation]

    # In case the white-points are still input as strings
    # Get white-points for illuminant
    if type(wp_src) == str:
        orig_illum = wp_src.lower()
        wp_src = color_constants.ILLUMINANTS[observer][orig_illum]
    elif hasattr(wp_src, '__iter__'):
        wp_src = wp_src

    if type(wp_dst) == str:
        targ_illum = wp_dst.lower()
        wp_dst = color_constants.ILLUMINANTS[observer][targ_illum]
    elif hasattr(wp_dst, '__iter__'):
        wp_dst = wp_dst

    # Sharpened cone responses ~ rho gamma beta ~ sharpened r g b
    rgb_src = numpy.dot(m_sharp, wp_src)
    rgb_dst = numpy.dot(m_sharp, wp_dst)

    # Ratio of whitepoint sharpened responses
    m_rat = numpy.diag(rgb_dst / rgb_src)

    # Final transformation matrix
    m_xfm = numpy.dot(numpy.dot(pinv(m_sharp), m_rat), m_sharp)

    return m_xfm


# noinspection PyPep8Naming
def apply_chromatic_adaptation(val_x, val_y, val_z, orig_illum, targ_illum,
                               observer='2', adaptation='bradford'):
    """
    Applies a chromatic adaptation matrix to convert XYZ values between
    illuminants. It is important to recognize that color transformation results
    in color errors, determined by how far the original illuminant is from the
    target illuminant. For example, D65 to A could result in very high maximum
    deviance.

    An informative article with estimate average Delta E values for each
    illuminant conversion may be found at:

    http://brucelindbloom.com/ChromAdaptEval.html
    """
    # It's silly to have to do this, but some people may want to call this
    # function directly, so we'll protect them from messing up upper/lower case.
    adaptation = adaptation.lower()

    # Get white-points for illuminant
    if type(orig_illum) == str:
        orig_illum = orig_illum.lower()
        wp_src = color_constants.ILLUMINANTS[observer][orig_illum]
    elif hasattr(orig_illum, '__iter__'):
        wp_src = orig_illum

    if type(targ_illum) == str:
        targ_illum = targ_illum.lower()
        wp_dst = color_constants.ILLUMINANTS[observer][targ_illum]
    elif hasattr(targ_illum, '__iter__'):
        wp_dst = targ_illum

    logger.debug("  \* Applying adaptation matrix: %s", adaptation)
    # Retrieve the appropriate transformation matrix from the constants.
    transform_matrix = _get_adaptation_matrix(wp_src, wp_dst,
                                              observer, adaptation)

    # Stuff the XYZ values into a NumPy matrix for conversion.
    XYZ_matrix = numpy.array((val_x, val_y, val_z))
    # Perform the adaptation via matrix multiplication.
    result_matrix = numpy.dot(transform_matrix, XYZ_matrix)

    # Return individual X, Y, and Z coordinates.
    return result_matrix[0], result_matrix[1], result_matrix[2]


# noinspection PyPep8Naming
def apply_chromatic_adaptation_on_color(color, targ_illum, adaptation='bradford'):
    """
    Convenience function to apply an adaptation directly to a Color object.
    """
    xyz_x = color.xyz_x
    xyz_y = color.xyz_y
    xyz_z = color.xyz_z
    orig_illum = color.illuminant
    targ_illum = targ_illum.lower()
    observer = color.observer
    adaptation = adaptation.lower()

    # Return individual X, Y, and Z coordinates.
    color.xyz_x, color.xyz_y, color.xyz_z = apply_chromatic_adaptation(
        xyz_x, xyz_y, xyz_z, orig_illum, targ_illum,
        observer=observer, adaptation=adaptation)
    color.set_illuminant(targ_illum)

    return color
