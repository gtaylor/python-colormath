"""
Color Difference Equations
""" 
from math import *

def delta_e_cie2000(color1, color2, Kl=1, Kc=1, Kh=1):
    """
    Calculates the CIE DeltaE 2000 of two colors.
    """
    # Color 1 
    L1 = color1.lab_l
    a1 = color1.lab_a
    b1 = color1.lab_b
    # Color 2
    L2 = color2.lab_l
    a2 = color2.lab_a
    b2 = color2.lab_b

    avg_Lp = (L1 + L2) / 2
    C1 = sqrt(pow(a1, 2) + pow(b1, 2))
    C2 = sqrt(pow(a2, 2) + pow(b2, 2))
    avg_C1_C2 = (C1 + C2) / 2.0 

    G = 0.5 * (1 - sqrt(pow(avg_C1_C2 , 7.0) / (pow(avg_C1_C2, 7.0) + pow(25.0, 7.0))))

    a1p = (1 + G) * a1
    a2p = (1 + G) * a2
    C1p = sqrt(pow(a1p, 2) + pow(b1, 2))
    C2p = sqrt(pow(a2p, 2) + pow(b2, 2))
    avg_C1p_C2p =(C1p + C2p) / 2
   
    if degrees(atan2(b1,a1p)) >= 0:
        h1p = degrees(atan2(b1,a1p))
    else:
        h1p = degrees(atan2(b1,a1p)) + 360
      
    if degrees(atan2(b2,a2p)) >= 0:
        h2p = degrees(atan2(b2,a2p))
    else:
        h2p = degrees(atan2(b2,a2p)) + 360
      
    if fabs(h1p - h2p) > 180:
        avg_Hp = (h1p + h2p + 360) / 2
    else:
        avg_Hp = (h1p + h2p) / 2

    T = 1 - 0.17 * cos(radians(avg_Hp - 30)) + 0.24 * cos(radians(2 * avg_Hp)) + 0.32 * cos(radians(3 * avg_Hp + 6)) - 0.2  * cos(radians(4 * avg_Hp - 63))

    diff_h2p_h1p = h2p - h1p    if fabs(diff_h2p_h1p) <= 180:
        delta_hp = diff_h2p_h1p
    elif (fabs(diff_h2p_h1p) > 180) and (h2p <= h1p):
        delta_hp = fabs(h1p - h2p) + 360
    elif (fabs(diff_h2p_h1p) > 180) and (h2p > h1p):
        delta_hp = fabs(h1p - h2p) - 360
      
    delta_Lp = L2 - L1
    delta_Cp = C2p - C1p
    delta_Hp = 2 * sqrt(C2p * C1p) * sin(radians(delta_hp) / 2.0)
   
    S_L = 1 + ((0.015 * pow(avg_Lp - 50, 2)) / sqrt(20 + pow(avg_Lp - 50, 2.0)))
    S_C = 1 + 0.045 * avg_C1p_C2p
    S_H = 1 + 0.015 * avg_C1p_C2p * T
   
    delta_ro = 30 * exp(-(pow(((avg_Hp - 275) / 25), 2.0)))
    R_C = sqrt((pow(avg_C1p_C2p, 7.0)) / (pow(avg_C1p_C2p, 7.0) + pow(25.0, 7.0)));
    R_T = -2 * R_C * sin(2 * radians(delta_ro))

    delta_E = sqrt(pow(delta_Lp /(S_L * Kl), 2) + pow(delta_Cp /(S_C * Kc), 2) + pow(delta_Hp /(S_H * Kh), 2) + R_T * (delta_Cp /(S_C * Kc)) * (delta_Hp / (S_H * Kh)))

    return delta_E