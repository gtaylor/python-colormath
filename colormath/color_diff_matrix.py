"""
Color Difference Equations for Matrices
"""
from .color_objects import LabColor

import numpy as np

def delta_e(lab_color, lab_color_matrix, mode='cie2000', *args, **kwargs):
    """
    Compares ........  via Delta E. The ... must be of shape ... and
    must be composed of LABColor objects. Implicit color-space conversion
    is not supported due to the cost of the operator. Returns a distance
    vector of shape (n,).

    Valid modes:
     cie2000
     cie1976
     cie1994
    """

    if not isinstance(lab_color, LabColor):
        raise InvalidArgument('delta_e', 'color_lab_scalar', color_lab_scalar)

    lab_color_vector = np.array([lab_color.lab_l, lab_color.lab_a, lab_color.lab_b])

    mode = mode.lower()

    if mode == 'cie2000':
        return _delta_e_cie2000(lab_color_vector, lab_color_matrix)
    elif mode == 'cie1994':
        return _delta_e_cie1994(lab_color_vector, lab_color_matrix, **kwargs)
    elif mode == 'cie1976':
        return _delta_e_cie1976(lab_color_vector, lab_color_matrix)
    else:
        raise InvalidDeltaEMode(mode)


def _delta_e_cie1976(lab_color_vector, lab_color_matrix):
    """
    Calculates the Delta E (CIE1976) of two colors.
    """
    return np.sqrt(np.sum(np.power(lab_color_vector - lab_color_matrix, 2), axis=1))


def _delta_e_cie1994(lab_color_vector, lab_color_matrix, K_L=1, K_C=1, K_H=1, K_1=0.045, K_2=0.015):
    """
    Calculates the Delta E (CIE1994) of two colors.

    K_l:
      0.045 graphic arts
      0.048 textiles
    K_2:
      0.015 graphic arts
      0.014 textiles
    K_L:
      1 default
      2 textiles
    """

    C_1 = np.sqrt(np.sum(np.power(lab_color_vector[1:], 2)))
    C_2 = np.sqrt(np.sum(np.power(lab_color_matrix[:,1:], 2), axis=1))

    delta_lab = lab_color_vector - lab_color_matrix
    delta_L = delta_lab[:,0].copy()

    delta_C = C_1 - C_2
    delta_lab[:,0] = delta_C

    delta_H_sq = np.sum(np.power(delta_lab,2) * np.array([-1,1,1]), axis=1)
    delta_H = np.sqrt(delta_H_sq.clip(min=0))

    S_L = 1
    S_C = 1 + K_1 * C_1
    S_H = 1 + K_2 * C_1

    L_group = np.power(delta_L / (K_L * S_L), 2)
    C_group = np.power(delta_C / (K_C * S_C), 2)
    H_group = np.power(delta_H / (K_H * S_H), 2)

    return np.sqrt(L_group + C_group + H_group)

