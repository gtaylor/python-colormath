"""
This module contains the formulas for comparing Lab values with matrices
and vectors. The benefit of using NumPy's matrix capabilities is speed. These
calls can be used to efficiently compare large volumes of Lab colors.
"""

import numpy


def delta_e_cie1976(lab_color_vector, lab_color_matrix):
    """
    Calculates the Delta E (CIE1976) between `lab_color_vector` and all
    colors in `lab_color_matrix`.
    """
    return numpy.sqrt(
        numpy.sum(numpy.power(lab_color_vector - lab_color_matrix, 2), axis=1))


# noinspection PyPep8Naming
def delta_e_cie1994(lab_color_vector, lab_color_matrix,
                    K_L=1, K_C=1, K_H=1, K_1=0.045, K_2=0.015):
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
    C_1 = numpy.sqrt(numpy.sum(numpy.power(lab_color_vector[1:], 2)))
    C_2 = numpy.sqrt(numpy.sum(numpy.power(lab_color_matrix[:, 1:], 2), axis=1))

    delta_lab = lab_color_vector - lab_color_matrix

    delta_L = delta_lab[:, 0].copy()
    delta_C = C_1 - C_2
    delta_lab[:, 0] = delta_C

    delta_H_sq = numpy.sum(numpy.power(delta_lab, 2) * numpy.array([-1, 1, 1]), axis=1)
    # noinspection PyArgumentList
    delta_H = numpy.sqrt(delta_H_sq.clip(min=0))

    S_L = 1
    S_C = 1 + K_1 * C_1
    S_H = 1 + K_2 * C_1

    LCH = numpy.vstack([delta_L, delta_C, delta_H])
    params = numpy.array([[K_L * S_L], [K_C * S_C], [K_H * S_H]])

    return numpy.sqrt(numpy.sum(numpy.power(LCH / params, 2), axis=0))


# noinspection PyPep8Naming
def delta_e_cmc(lab_color_vector, lab_color_matrix, pl=2, pc=1):
    """
    Calculates the Delta E (CIE1994) of two colors.

    CMC values
      Acceptability: pl=2, pc=1
      Perceptability: pl=1, pc=1
    """
    L, a, b = lab_color_vector

    C_1 = numpy.sqrt(numpy.sum(numpy.power(lab_color_vector[1:], 2)))
    C_2 = numpy.sqrt(numpy.sum(numpy.power(lab_color_matrix[:, 1:], 2), axis=1))

    delta_lab = lab_color_vector - lab_color_matrix

    delta_L = delta_lab[:, 0].copy()
    delta_C = C_1 - C_2
    delta_lab[:, 0] = delta_C

    H_1 = numpy.degrees(numpy.arctan2(b, a))

    if H_1 < 0:
        H_1 += 360

    F = numpy.sqrt(numpy.power(C_1, 4) / (numpy.power(C_1, 4) + 1900.0))

    # noinspection PyChainedComparisons
    if 164 <= H_1 and H_1 <= 345:
        T = 0.56 + abs(0.2 * numpy.cos(numpy.radians(H_1 + 168)))
    else:
        T = 0.36 + abs(0.4 * numpy.cos(numpy.radians(H_1 + 35)))

    if L < 16:
        S_L = 0.511
    else:
        S_L = (0.040975 * L) / (1 + 0.01765 * L)

    S_C = ((0.0638 * C_1) / (1 + 0.0131 * C_1)) + 0.638
    S_H = S_C * (F * T + 1 - F)

    delta_C = C_1 - C_2

    delta_H_sq = numpy.sum(numpy.power(delta_lab, 2) * numpy.array([-1, 1, 1]), axis=1)
    # noinspection PyArgumentList
    delta_H = numpy.sqrt(delta_H_sq.clip(min=0))

    LCH = numpy.vstack([delta_L, delta_C, delta_H])
    params = numpy.array([[pl * S_L], [pc * S_C], [S_H]])

    return numpy.sqrt(numpy.sum(numpy.power(LCH / params, 2), axis=0))


# noinspection PyPep8Naming
def delta_e_cie2000(lab_color_vector, lab_color_matrix, Kl=1, Kc=1, Kh=1):
    """
    Calculates the Delta E (CIE2000) of two colors.
    """
    L, a, b = lab_color_vector

    avg_Lp = (L + lab_color_matrix[:, 0]) / 2.0

    C1 = numpy.sqrt(numpy.sum(numpy.power(lab_color_vector[1:], 2)))
    C2 = numpy.sqrt(numpy.sum(numpy.power(lab_color_matrix[:, 1:], 2), axis=1))

    avg_C1_C2 = (C1 + C2) / 2.0

    G = 0.5 * (1 - numpy.sqrt(numpy.power(avg_C1_C2, 7.0) / (numpy.power(avg_C1_C2, 7.0) + numpy.power(25.0, 7.0))))

    a1p = (1.0 + G) * a
    a2p = (1.0 + G) * lab_color_matrix[:, 1]

    C1p = numpy.sqrt(numpy.power(a1p, 2) + numpy.power(b, 2))
    C2p = numpy.sqrt(numpy.power(a2p, 2) + numpy.power(lab_color_matrix[:, 2], 2))

    avg_C1p_C2p = (C1p + C2p) / 2.0

    h1p = numpy.degrees(numpy.arctan2(b, a1p))
    h1p += (h1p < 0) * 360

    h2p = numpy.degrees(numpy.arctan2(lab_color_matrix[:, 2], a2p))
    h2p += (h2p < 0) * 360

    avg_Hp = (((numpy.fabs(h1p - h2p) > 180) * 360) + h1p + h2p) / 2.0

    T = 1 - 0.17 * numpy.cos(numpy.radians(avg_Hp - 30)) + \
        0.24 * numpy.cos(numpy.radians(2 * avg_Hp)) + \
        0.32 * numpy.cos(numpy.radians(3 * avg_Hp + 6)) - \
        0.2 * numpy.cos(numpy.radians(4 * avg_Hp - 63))

    diff_h2p_h1p = h2p - h1p
    delta_hp = diff_h2p_h1p + (numpy.fabs(diff_h2p_h1p) > 180) * 360
    delta_hp -= (h2p > h1p) * 720

    delta_Lp = lab_color_matrix[:, 0] - L
    delta_Cp = C2p - C1p
    delta_Hp = 2 * numpy.sqrt(C2p * C1p) * numpy.sin(numpy.radians(delta_hp) / 2.0)

    S_L = 1 + ((0.015 * numpy.power(avg_Lp - 50, 2)) / numpy.sqrt(20 + numpy.power(avg_Lp - 50, 2.0)))
    S_C = 1 + 0.045 * avg_C1p_C2p
    S_H = 1 + 0.015 * avg_C1p_C2p * T

    delta_ro = 30 * numpy.exp(-(numpy.power(((avg_Hp - 275) / 25), 2.0)))
    R_C = numpy.sqrt((numpy.power(avg_C1p_C2p, 7.0)) / (numpy.power(avg_C1p_C2p, 7.0) + numpy.power(25.0, 7.0)))
    R_T = -2 * R_C * numpy.sin(2 * numpy.radians(delta_ro))

    return numpy.sqrt(
        numpy.power(delta_Lp / (S_L * Kl), 2) +
        numpy.power(delta_Cp / (S_C * Kc), 2) +
        numpy.power(delta_Hp / (S_H * Kh), 2) +
        R_T * (delta_Cp / (S_C * Kc)) * (delta_Hp / (S_H * Kh)))
