"""
Color Difference Equations for Matrices. This is a direct port of the functions
in color_diff.py. There is opportunity for optimisation especially for the more
complex deltaE functions

Eddie Bell - ejlbell@gmail.com - 17/01/14
"""

import numpy as np

def delta_e_cie1976(lab_color_vector, lab_color_matrix):
    """
    Calculates the Delta E (CIE1976) between `lab_color_vector` and all
    colors in `lab_color_matrix`.
    """
    return np.sqrt(np.sum(np.power(lab_color_vector - lab_color_matrix, 2), axis=1))


def delta_e_cie1994(lab_color_vector, lab_color_matrix, K_L=1, K_C=1, K_H=1, K_1=0.045, K_2=0.015):
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

    delta_H_sq = np.sum(np.power(delta_lab, 2) * np.array([-1,1,1]), axis=1)
    delta_H = np.sqrt(delta_H_sq.clip(min=0))

    S_L = 1
    S_C = 1 + K_1 * C_1
    S_H = 1 + K_2 * C_1

    LCH = np.vstack([delta_L, delta_C, delta_H])
    params = np.array([[K_L * S_L], [K_C * S_C], [K_H * S_H]])

    return np.sqrt(np.sum(np.power(LCH / params, 2), axis=0))


def delta_e_cmc(lab_color_vector, lab_color_matrix, pl=2, pc=1):
    """
    Calculates the Delta E (CIE1994) of two colors.

    CMC values
      Acceptability: pl=2, pc=1
      Perceptability: pl=1, pc=1
    """

    L, a, b  = lab_color_vector

    C_1 = np.sqrt(np.sum(np.power(lab_color_vector[1:], 2)))
    C_2 = np.sqrt(np.sum(np.power(lab_color_matrix[:,1:], 2), axis=1))

    delta_lab = lab_color_vector - lab_color_matrix

    delta_L = delta_lab[:,0].copy()
    delta_C = C_1 - C_2
    delta_lab[:,0] = delta_C

    H_1 = np.degrees(np.arctan2(b, a))

    if H_1 < 0:
        H_1 = H_1 + 360

    F = np.sqrt(np.power(C_1, 4) / (np.power(C_1, 4) + 1900.0))

    if 164 <= H_1 and H_1 <= 345:
        T = 0.56 + abs(0.2 * np.cos(np.radians(H_1 + 168)))
    else:
        T = 0.36 + abs(0.4 * np.cos(np.radians(H_1 + 35)))

    if L < 16:
        S_L = 0.511
    else:
        S_L = (0.040975 * L) / (1 + 0.01765 * L)

    S_C = ((0.0638 * C_1) / (1 + 0.0131 * C_1)) + 0.638
    S_H = S_C * (F * T + 1 - F)

    delta_C = C_1 - C_2

    delta_H_sq = np.sum(np.power(delta_lab, 2) * np.array([-1,1,1]), axis=1)
    delta_H = np.sqrt(delta_H_sq.clip(min=0))

    LCH = np.vstack([delta_L, delta_C, delta_H])
    params = np.array([[pl * S_L], [pc * S_C], [S_H]])

    return np.sqrt(np.sum(np.power(LCH / params, 2), axis=0))


def delta_e_cie2000(lab_color_vector, lab_color_matrix, Kl=1, Kc=1, Kh=1):
    """
    Calculates the Delta E (CIE2000) of two colors.
    """
    L, a, b  = lab_color_vector

    avg_Lp = (L + lab_color_matrix[:,0]) / 2.0

    C1 = np.sqrt(np.sum(np.power(lab_color_vector[1:], 2)))
    C2 = np.sqrt(np.sum(np.power(lab_color_matrix[:,1:], 2), axis=1))

    avg_C1_C2 = (C1 + C2) / 2.0

    G = 0.5 * (1 - np.sqrt(np.power(avg_C1_C2 , 7.0) / (np.power(avg_C1_C2, 7.0) + np.power(25.0, 7.0))))

    a1p = (1.0 + G) * a
    a2p = (1.0 + G) * lab_color_matrix[:, 1]

    C1p = np.sqrt(np.power(a1p, 2) + np.power(b, 2))
    C2p = np.sqrt(np.power(a2p, 2) + np.power(lab_color_matrix[:,2], 2))

    avg_C1p_C2p =(C1p + C2p) / 2.0

    h1p = np.degrees(np.arctan2(b, a1p))
    h1p = h1p + (h1p < 0) * 360

    h2p = np.degrees(np.arctan2(lab_color_matrix[:,2], a2p))
    h2p = h2p + (h2p < 0) * 360

    avg_Hp = (((np.fabs(h1p - h2p ) > 180) * 360) + h1p + h2p) / 2.0

    T = 1 - 0.17 * np.cos(np.radians(avg_Hp - 30)) + \
            0.24 * np.cos(np.radians(2 * avg_Hp)) + \
            0.32 * np.cos(np.radians(3 * avg_Hp + 6)) - \
            0.2  * np.cos(np.radians(4 * avg_Hp - 63))

    diff_h2p_h1p = h2p - h1p
    delta_hp = diff_h2p_h1p + (diff_h2p_h1p > 180) * 360
    delta_hp = delta_hp - (h2p > h1p) * 720

    delta_Lp = lab_color_matrix[:,0] - L
    delta_Cp = C2p - C1p
    delta_Hp = 2 * np.sqrt(C2p * C1p) * np.sin(np.radians(delta_hp) / 2.0)

    S_L = 1 + ((0.015 * np.power(avg_Lp - 50, 2)) / np.sqrt(20 + np.power(avg_Lp - 50, 2.0)))
    S_C = 1 + 0.045 * avg_C1p_C2p
    S_H = 1 + 0.015 * avg_C1p_C2p * T

    delta_ro = 30 * np.exp(-(np.power(((avg_Hp - 275) / 25), 2.0)))
    R_C = np.sqrt((np.power(avg_C1p_C2p, 7.0)) / (np.power(avg_C1p_C2p, 7.0) + np.power(25.0, 7.0)));
    R_T = -2 * R_C * np.sin(2 * np.radians(delta_ro))

    return np.sqrt(np.power(delta_Lp /(S_L * Kl), 2) +
                   np.power(delta_Cp /(S_C * Kc), 2) +
                   np.power(delta_Hp /(S_H * Kh), 2) +
                   R_T * (delta_Cp /(S_C * Kc)) * (delta_Hp / (S_H * Kh)))

