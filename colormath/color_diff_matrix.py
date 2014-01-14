"""
Color Difference Equations for Matrices
"""
import numpy as np

def delta_e_cie1976(lab_color_vector, lab_color_matrix):
    """
    Calculates the Delta E (CIE1976) between `lab_color_vector` and all
    colors in `lab_color_matrix`.
    """

    # euclidean distance
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


def delta_e_cie2000(lab_color_vector, lab_color_matrix, Kl=1, Kc=1, Kh=1):
    """
    DOES NOT WORK
    #############################
    Calculates the Delta E (CIE2000) of two colors.
    ############################
    DOES NOT WORK
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
    h1p[h1p<0] += 360

    h2p = np.degrees(np.arctan2(lab_color_matrix[:,2], a2p))
    h2p[h2p<0] += 360

    avg_Hp = np.fabs(h1p - h2p)
    avg_Hp[fabs>180] = ((h1p + h2p + 360) / 2.0)[fabs>180]
    avg_Hp[fabs<=180] = ((h1p + h2p) / 2.0)[fabs<=180]

    T = 1 - 0.17 * np.cos(np.radians(avg_Hp - 30)) + \
            0.24 * np.cos(np.radians(2 * avg_Hp)) + \
            0.32 * np.cos(np.radians(3 * avg_Hp + 6)) - \
            0.2  * np.cos(np.radians(4 * avg_Hp - 63))

    diff_h2p_h1p = h2p - h1p

    ###################
    ### NEEDS FIXING HERE AND TESTING
    ##################

    if np.fabs(diff_h2p_h1p) <= 180:
        delta_hp = diff_h2p_h1p
    elif (np.fabs(diff_h2p_h1p) > 180) and (h2p <= h1p):
        delta_hp = diff_h2p_h1p + 360
    else:
        delta_hp = diff_h2p_h1p - 360

    delta_Lp = L2 - L1
    delta_Cp = C2p - C1p
    delta_Hp = 2 * np.sqrt(C2p * C1p) * np.sin(np.radians(delta_hp) / 2.0)

    S_L = 1 + ((0.015 * np.power(avg_Lp - 50, 2)) / np.sqrt(20 + np.power(avg_Lp - 50, 2.0)))
    S_C = 1 + 0.045 * avg_C1p_C2p
    S_H = 1 + 0.015 * avg_C1p_C2p * T

    delta_ro = 30 * np.exp(-(np.power(((avg_Hp - 275) / 25), 2.0)))
    R_C = np.sqrt((np.power(avg_C1p_C2p, 7.0)) / (np.power(avg_C1p_C2p, 7.0) + np.power(25.0, 7.0)));
    R_T = -2 * R_C * np.sin(2 * np.radians(delta_ro))

    delta_E = np.sqrt(np.power(delta_Lp /(S_L * Kl), 2) +
                      np.power(delta_Cp /(S_C * Kc), 2) +
                      np.power(delta_Hp /(S_H * Kh), 2) +
                      R_T * (delta_Cp /(S_C * Kc)) * (delta_Hp / (S_H * Kh)))
    return delta_E

def delta_e_cmc(color_lab_vector, color_lab_matrix, pl=2, pc=1):
    """
    Does not work
    ###########################
    Calculates the Delta E (CIE1994) of two colors.

    CMC values
      Acceptability: pl=2, pc=1
      Perceptability: pl=1, pc=1
    ######################
    Does not work
    """
    # Color 1
    L1 = float(color1.lab_l)
    a1 = float(color1.lab_a)
    b1 = float(color1.lab_b)
    # Color 2
    L2 = float(color2.lab_l)
    a2 = float(color2.lab_a)
    b2 = float(color2.lab_b)

    delta_L = L1 - L2
    delta_a = a1 - a2
    delta_b = b1 - b2

    C_1 = sqrt(pow(a1, 2) + pow(b1, 2))
    C_2 = sqrt(pow(a2, 2) + pow(b2, 2))

    H_1 = degrees(atan2(b1, a1))

    if H_1 < 0:
        H_1 = H_1 + 360

    F = sqrt(pow(C_1, 4) / (pow(C_1, 4) + 1900.0))
    if 164 <= H_1 and H_1 <= 345:
        T = 0.56 + abs(0.2 * cos(radians(H_1 + 168)))
    else:
        T = 0.36 + abs(0.4 * cos(radians(H_1 + 35)))

    if L1 < 16:
        S_L = 0.511
    else:
        S_L = (0.040975 * L1) / (1 + 0.01765 * L1)
    S_C = ((0.0638 * C_1) / (1 + 0.0131 * C_1)) + 0.638
    S_H = S_C * (F * T + 1 - F)

    delta_C = C_1 - C_2
    try:
        delta_H = sqrt(pow(delta_a, 2) + pow(delta_b, 2) - pow(delta_C, 2))
    except ValueError:
        delta_H = 0.0

    L_group = delta_L / (pl * S_L)
    C_group = delta_C / (pc * S_C)
