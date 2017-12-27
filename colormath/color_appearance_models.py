"""
Copyright (c) 2014, Michael Mauderer, University of St Andrews
All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

 * Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.
 * Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.
 * Neither the name of the University of St Andrews nor the names of its
   contributors may be used to endorse or promote products derived from this
   software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from __future__ import division

import logging
import numpy

logger = logging.getLogger(__name__)


class Nayatani95(object):
    """
    **References**

    * Fairchild, M. D. (2013). *Color appearance models*, 3rd Ed. John Wiley & Sons.
    * Nayatani, Y., Sobagaki, H., & Yano, K. H. T. (1995). Lightness dependency of chroma scales of a nonlinear
      color-appearance model and its latest formulation. *Color Research & Application*, 20(3), 156-167.

    """

    @property
    def hue_angle(self):
        """
        Predicted hue angle :math:`\\theta`.
        """
        return self._hue_angle

    @property
    def chroma(self):
        """
        Predicted chroma :math:`C`.
        """
        return self._chroma

    @property
    def saturation(self):
        """
        Predicted saturation :math:`S`.
        """
        return self._saturation

    @property
    def brightness(self):
        """
        Predicted brightness :math:`B_r`.
        """
        return self._brightness

    @property
    def colorfulness(self):
        """
        Predicted colorfulness :math:`M`.
        """
        return self._colorfulness

    def __init__(self, x, y, z, x_n, y_n, z_n, y_ob, e_o, e_or, n=1):
        """
        :param x: X value of test sample :math:`X`.
        :param y: Y value of test sample :math:`Y`.
        :param z: Z value of test sample :math:`Z`.
        :param x_n: X value of reference white :math:`X_n`.
        :param y_n: Y value of reference white :math:`Y_n`.
        :param z_n: Z value of reference white :math:`Z_n`.
        :param y_ob: Luminance factor of achromatic background as percentage :math:`Y_o`.
                     Required to be larger than 0.18.
        :param e_o: Illuminance of the viewing field :math:`E_o` in lux.
        :param e_or: Normalising illuminance :math:`E_or` in lux.
        :param n: Noise term :math:`n`.
        """

        if numpy.any(y_ob <= 0.18):
            raise ValueError('y_ob hast be greater than 0.18.')

        l_o = y_ob * e_o / (100 * numpy.pi)
        l_or = y_ob * e_or / (100 * numpy.pi)
        logger.debug('L_o: {}'.format(l_o))
        logger.debug('L_or: {}'.format(l_or))

        x_o = x_n / (x_n + y_n + z_n)
        y_o = y_n / (x_n + y_n + z_n)
        logger.debug('x_o: {}'.format(x_o))
        logger.debug('y_o: {}'.format(y_o))

        xi = (0.48105 * x_o + 0.78841 * y_o - 0.08081) / y_o
        eta = (-0.27200 * x_o + 1.11962 * y_o + 0.04570) / y_o
        zeta = (0.91822 * (1 - x_o - y_o)) / y_o
        logger.debug('xi: {}'.format(xi))
        logger.debug('eta: {}'.format(eta))
        logger.debug('zeta: {}'.format(zeta))

        r_0, g_0, b_0 = rgb_0 = ((y_ob * e_o) / (100 * numpy.pi)) * numpy.array([xi, eta, zeta])
        logger.debug('rgb_0: {}'.format(rgb_0))

        r, g, b, = rgb = self.xyz_to_rgb(numpy.array([x, y, z]))
        logger.debug('rgb: {}'.format(rgb))

        e_r = self._compute_scaling_coefficient(r, xi)
        logger.debug('e(R): {}'.format(e_r))
        e_g = self._compute_scaling_coefficient(g, eta)
        logger.debug('e(G): {}'.format(e_g))

        beta_r = self._beta_1(r_0)
        logger.debug('beta1(rho): {}'.format(beta_r))
        beta_g = self._beta_1(g_0)
        logger.debug('beta1(eta): {}'.format(beta_g))
        beta_b = self._beta_2(b_0)
        logger.debug('beta2(zeta): {}'.format(beta_b))

        beta_l = self._beta_1(l_or)
        logger.debug('beta1(L_or): {}'.format(beta_l))

        # Opponent Color Dimension
        self._achromatic_response = (2 / 3) * beta_r * e_r * numpy.log10((r + n) / (20 * xi + n))
        self._achromatic_response += (1 / 3) * beta_g * e_g * numpy.log10((g + n) / (20 * eta + n))
        self._achromatic_response *= 41.69 / beta_l
        logger.debug('Q: {}'.format(self._achromatic_response))

        self._tritanopic_response = (1 / 1) * beta_r * numpy.log10((r + n) / (20 * xi + n))
        self._tritanopic_response += - (12 / 11) * beta_g * numpy.log10((g + n) / (20 * eta + n))
        self._tritanopic_response += (1 / 11) * beta_b * numpy.log10((b + n) / (20 * zeta + n))
        logger.debug('t: {}'.format(self._tritanopic_response))

        self._protanopic_response = (1 / 9) * beta_r * numpy.log10((r + n) / (20 * xi + n))
        self._protanopic_response += (1 / 9) * beta_g * numpy.log10((g + n) / (20 * eta + n))
        self._protanopic_response += - (2 / 9) * beta_b * numpy.log10((b + n) / (20 * zeta + n))
        logger.debug('p: {}'.format(self._protanopic_response))

        # Brightness
        self._brightness = (50 / beta_l) * ((2 / 3) * beta_r + (1 / 3) * beta_g) + self._achromatic_response

        self._brightness_ideal_white = (2 / 3) * beta_r * 1.758 * numpy.log10((100 * xi + n) / (20 * xi + n))
        self._brightness_ideal_white += (1 / 3) * beta_g * 1.758 * numpy.log10((100 * eta + n) / (20 * eta + n))
        self._brightness_ideal_white *= 41.69 / beta_l
        self._brightness_ideal_white += (50 / beta_l) * (2 / 3) * beta_r
        self._brightness_ideal_white += (50 / beta_l) * (1 / 3) * beta_g

        # Lightness
        self._lightness_achromatic = self._achromatic_response + 50
        self._lightness_achromatic_normalized = 100 * (self._brightness / self._brightness_ideal_white)

        # Hue
        hue_angle_rad = numpy.arctan2(self._protanopic_response, self._tritanopic_response)
        self._hue_angle = ((360 * hue_angle_rad / (2 * numpy.pi)) + 360) % 360
        logger.debug('theta: {}'.format(self._hue_angle))

        e_s_theta = self.chromatic_strength(hue_angle_rad)
        logger.debug('E_s(theta): {}'.format(e_s_theta))

        # Saturation
        self._saturation_rg = (488.93 / beta_l) * e_s_theta * self._tritanopic_response
        self._saturation_yb = (488.93 / beta_l) * e_s_theta * self._protanopic_response
        logger.debug('S_RG: {}'.format(self._saturation_rg))
        logger.debug('S_YB: {}'.format(self._saturation_yb))

        self._saturation = numpy.sqrt((self._saturation_rg ** 2) + (self._saturation_yb ** 2))
        logger.debug('S: {}'.format(self._saturation))

        # Chroma
        self._chroma_rg = ((self._lightness_achromatic / 50) ** 0.7) * self._saturation_rg
        self._chroma_yb = ((self._lightness_achromatic / 50) ** 0.7) * self._saturation_yb
        self._chroma = ((self._lightness_achromatic / 50) ** 0.7) * self._saturation
        logger.debug('C: {}'.format(self._chroma))

        # Colorfulness
        self._colorfulness_rg = self._chroma_rg * self._brightness_ideal_white / 100
        self._colorfulness_yb = self._chroma_yb * self._brightness_ideal_white / 100
        self._colorfulness = self._chroma * self._brightness_ideal_white / 100

    @staticmethod
    def chromatic_strength(angle):
        result = 0.9394
        result += - 0.2478 * numpy.sin(1 * angle)
        result += - 0.0743 * numpy.sin(2 * angle)
        result += + 0.0666 * numpy.sin(3 * angle)
        result += - 0.0186 * numpy.sin(4 * angle)
        result += - 0.0055 * numpy.cos(1 * angle)
        result += - 0.0521 * numpy.cos(2 * angle)
        result += - 0.0573 * numpy.cos(3 * angle)
        result += - 0.0061 * numpy.cos(4 * angle)
        return result

    @staticmethod
    def _compute_scaling_coefficient(a, b):
        return numpy.where(a >= (20 * b), 1.758, 1)

    @staticmethod
    def _beta_1(x):
        return (6.469 + 6.362 * (x ** 0.4495)) / (6.469 + (x ** 0.4495))

    @staticmethod
    def _beta_2(x):
        return 0.7844 * (8.414 + 8.091 * (x ** 0.5128)) / (8.414 + (x ** 0.5128))

    xyz_to_rgb_m = numpy.array([[0.40024, 0.70760, -0.08081],
                                [-0.22630, 1.16532, 0.04570],
                                [0, 0, 0.91822]])

    @classmethod
    def xyz_to_rgb(cls, xyz):
        return cls.xyz_to_rgb_m.dot(xyz)


class Hunt(object):
    """
    **References**

    * Fairchild, M. D. (2013). *Color appearance models*, 3rd Ed. John Wiley & Sons.
    * Hunt, R. W. G. (2005). *The reproduction of colour*. 5th Ed., John Wiley & Sons.

    """

    @property
    def hue_angle(self):
        """
        Predicted hue angle :math:`h_s`.
        """
        return self._hue_angle

    @property
    def chroma(self):
        """
        Predicted chroma :math:`C_{94}`.
        """
        return self._chroma

    @property
    def saturation(self):
        """
        Predicted saturation :math:`s`.
        """
        return self._saturation

    @property
    def brightness(self):
        """
        Predicted brightness :math:`Q`.
        """
        return self._brightness

    @property
    def colorfulness(self):
        """
        Predicted colorfulness :math:`M_{94}`.
        """
        return self._colorfulness

    @property
    def lightness(self):
        """
        Predicted colorfulness :math:`J`.
        """
        return self._lightness

    def __init__(self, x, y, z,
                 x_b, y_b, z_b,
                 x_w, y_w, z_w,
                 l_a,
                 n_c,
                 n_b,
                 l_as=None,
                 cct_w=None,
                 n_cb=None,
                 n_bb=None,
                 x_p=None,
                 y_p=None,
                 z_p=None,
                 p=None,
                 helson_judd=False,
                 discount_illuminant=True,
                 s=None,
                 s_w=None):
        """
        :param x: X value of test sample :math:`X`.
        :param y: Y value of test sample :math:`Y`.
        :param z: Z value of test sample :math:`Z`.
        :param x_b: X value of background :math:`X_b`.
        :param y_b: Y value of background :math:`Y_b`.
        :param z_b: Z value of background :math:`Z_b`.
        :param x_w: X value of reference white :math:`X_W`.
        :param y_w: Y value of reference white :math:`Y_W`.
        :param z_w: Z value of reference white :math:`Z_W`.
        :param l_a: Adapting luminance :math:`L_A`.
        :param n_c: Chromatic surround induction_factor :math:`N_c`.
        :param n_b: Brightness surround induction factor :math:`N_b`.
        :param l_as: Scotopic luminance of the illuminant :math:`L_{AS}`.
                     Will be approximated if not supplied.
        :param cct_w: Correlated color temperature of illuminant :math:`T`.
                      Will be used to approximate l_as if not supplied.
        :param n_cb: Chromatic background induction factor :math:`N_{cb}`.
                     Will be approximated using y_w and y_b if not supplied.
        :param n_bb: Brightness background induction factor :math:`N_{bb}`.
                     Will be approximated using y_w and y_b if not supplied.
        :param x_p: X value of proxima field :math:`X_p`.
                    If not supplied, will be assumed to equal background.
        :param y_p: Y value of proxima field :math:`Y_p`.
                    If not supplied, will be assumed to equal background.
        :param z_p: Z value of proxima field :math:`Z_p`.
                    If not supplied, will be assumed to equal background.
        :param p: Simultaneous contrast/assimilation parameter.
        :param helson_judd: Truth value indicating whether the Heslon-Judd effect should be accounted for.
                            Default False.
        :param discount_illuminant: Truth value whether discount-the-illuminant should be applied. Default True.
        :param s: Scotopic response to the stimulus.
        :param s_w: Scotopic response for th reference white.
        :raises ValueError: if illegal parameter combination is supplied.
        """
        if x_p is None:
            x_p = x_b
            logger.warn('Approximated x_p with x_b.')
        if y_p is None:
            y_p = y_b
            logger.warn('Approximated y_p with y_b.')
        if z_p is None:
            z_p = y_b
            logger.warn('Approximated z_p with z_b.')

        if n_cb is None:
            n_cb = 0.725 * (y_w / y_b) ** 0.2
            logger.warn('Approximated n_cb.')
        logger.debug('N_cb: {}'.format(n_cb))
        if n_bb is None:
            n_bb = 0.725 * (y_w / y_b) ** 0.2
            logger.warn('Approximated n_bb.')
        logger.debug('N_bb: {}'.format(n_cb))

        if l_as is None:
            logger.warn('Approximated scotopic luminance.')
            if cct_w is None:
                cct_w = self._get_cct(x_w, y_w, z_w)
                logger.warn('Approximated cct_w: {}'.format(cct_w))
            l_as = 2.26 * l_a
            l_as *= ((cct_w / 4000) - 0.4) ** (1 / 3)
        logger.debug('LA_S: {}'.format(l_as))

        if s is None != s_w is None:
            raise ValueError("Either both scotopic responses (s, s_w) need to be supplied or none.")
        elif s is None and s_w is None:
            s = y
            s_w = y_w
            logger.warn('Approximated scotopic response to stimulus and reference white.')

        if p is None:
            logger.warn('p not supplied. Model will not account for simultaneous chromatic contrast .')

        xyz = numpy.array([x, y, z])
        logger.debug('XYZ: {}'.format(xyz))
        xyz_w = numpy.array([x_w, y_w, z_w])
        logger.debug('XYZ_W: {}'.format(xyz_w))
        xyz_b = numpy.array([x_b, y_b, z_b])
        xyz_p = numpy.array([x_p, y_p, z_p])

        k = 1 / (5 * l_a + 1)
        logger.debug('k: {}'.format(k))
        # luminance adaptation factor
        f_l = 0.2 * (k ** 4) * (5 * l_a) + 0.1 * ((1 - (k ** 4)) ** 2) * ((5 * l_a) ** (1 / 3))
        logger.debug('F_L: {}'.format(f_l))

        logger.debug('--- Stimulus RGB adaptation start ----')
        rgb_a = self._adaptation(f_l, l_a, xyz, xyz_w, xyz_b, xyz_p, p, helson_judd, discount_illuminant)
        logger.debug('--- Stimulus RGB adaptation end ----')
        r_a, g_a, b_a = rgb_a
        logger.debug('RGB_A: {}'.format(rgb_a))
        logger.debug('--- White RGB adaptation start ----')
        rgb_aw = self._adaptation(f_l, l_a, xyz_w, xyz_w, xyz_b, xyz_p, p, helson_judd, discount_illuminant)
        logger.debug('--- White RGB adaptation end ----')
        r_aw, g_aw, b_aw = rgb_aw
        logger.debug('RGB_AW: {}'.format(rgb_aw))

        # ---------------------------
        # Opponent Color Dimensions
        # ---------------------------

        # achromatic_cone_signal
        a_a = 2 * r_a + g_a + (1 / 20) * b_a - 3.05 + 1
        logger.debug('A_A: {}'.format(a_a))
        a_aw = 2 * r_aw + g_aw + (1 / 20) * b_aw - 3.05 + 1
        logger.debug('A_AW: {}'.format(a_aw))

        c1 = r_a - g_a
        logger.debug('C1: {}'.format(c1))
        c2 = g_a - b_a
        logger.debug('C2: {}'.format(c2))
        c3 = b_a - r_a
        logger.debug('C3: {}'.format(c3))

        c1_w = r_aw - g_aw
        logger.debug('C1_W: {}'.format(c1_w))
        c2_w = g_aw - b_aw
        logger.debug('C2_W: {}'.format(c2_w))
        c3_w = b_aw - r_aw
        logger.debug('C3_W: {}'.format(c3_w))

        # -----
        # Hue
        # -----
        self._hue_angle = (180 * numpy.arctan2(0.5 * (c2 - c3) / 4.5, c1 - (c2 / 11)) / numpy.pi) % 360
        hue_angle_w = (180 * numpy.arctan2(0.5 * (c2_w - c3_w) / 4.5, c1_w - (c2_w / 11)) / numpy.pi) % 360

        # -------------
        # Saturation
        # -------------
        e_s = self._calculate_eccentricity_factor(self.hue_angle)
        logger.debug('es: {}'.format(e_s))
        e_s_w = self._calculate_eccentricity_factor(hue_angle_w)

        f_t = l_a / (l_a + 0.1)
        logger.debug('F_t: {}'.format(f_t))
        m_yb = 100 * (0.5 * (c2 - c3) / 4.5) * (e_s * (10 / 13) * n_c * n_cb * f_t)
        logger.debug('m_yb: {}'.format(m_yb))
        m_rg = 100 * (c1 - (c2 / 11)) * (e_s * (10 / 13) * n_c * n_cb)
        logger.debug('m_rg: {}'.format(m_rg))
        m = ((m_rg ** 2) + (m_yb ** 2)) ** 0.5
        logger.debug('m: {}'.format(m))

        self._saturation = 50 * m / rgb_a.sum(axis=0)

        m_yb_w = 100 * (0.5 * (c2_w - c3_w) / 4.5) * (e_s_w * (10 / 13) * n_c * n_cb * f_t)
        m_rg_w = 100 * (c1_w - (c2_w / 11)) * (e_s_w * (10 / 13) * n_c * n_cb)
        m_w = ((m_rg_w ** 2) + (m_yb_w ** 2)) ** 0.5

        # ------------
        # Brightness
        # ------------
        logger.debug('--- Stimulus achromatic signal START ----')
        a = self._calculate_achromatic_signal(l_as, s, s_w, n_bb, a_a)
        logger.debug('--- Stimulus achromatic signal END ----')
        logger.debug('A: {}'.format(a))

        logger.debug('--- White achromatic signal START ----')
        a_w = self._calculate_achromatic_signal(l_as, s_w, s_w, n_bb, a_aw)
        logger.debug('--- White achromatic signal END ----')
        logger.debug('A_w: {}'.format(a_w))

        n1 = ((7 * a_w) ** 0.5) / (5.33 * n_b ** 0.13)
        n2 = (7 * a_w * n_b ** 0.362) / 200
        logger.debug('N1: {}'.format(n1))
        logger.debug('N2: {}'.format(n2))

        self._brightness = ((7 * (a + (m / 100))) ** 0.6) * n1 - n2
        brightness_w = ((7 * (a_w + (m_w / 100))) ** 0.6) * n1 - n2
        logger.debug('Q: {}'.format(self.brightness))
        logger.debug('Q_W: {}'.format(brightness_w))

        # ----------
        # Lightness
        # ----------
        z = 1 + (y_b / y_w) ** 0.5
        logger.debug('z: {}'.format(z))
        self._lightness = 100 * (self.brightness / brightness_w) ** z

        # -------
        # Chroma
        # -------
        self._chroma = 2.44 * (self.saturation ** 0.69) * ((self.brightness / brightness_w) ** (y_b / y_w)) * (
            1.64 - 0.29 ** (y_b / y_w))

        # -------------
        # Colorfulness
        # -------------
        self._colorfulness = (f_l ** 0.15) * self.chroma

    xyz_to_rgb_m = numpy.array([[0.38971, 0.68898, -0.07868],
                                [-0.22981, 1.18340, 0.04641],
                                [0, 0, 1]])

    @classmethod
    def xyz_to_rgb(cls, xyz):
        return cls.xyz_to_rgb_m.dot(xyz)

    def _adaptation(self, f_l, l_a, xyz, xyz_w, xyz_b, xyz_p=None, p=None, helson_judd=False, discount_illuminant=True):
        """
        :param f_l: Luminance adaptation factor
        :param l_a: Adapting luminance
        :param xyz: Stimulus color in XYZ
        :param xyz_w: Reference white color in XYZ
        :param xyz_b: Background color in XYZ
        :param xyz_p: Proxima field color in XYZ
        :param p: Simultaneous contrast/assimilation parameter.
        """
        rgb = self.xyz_to_rgb(xyz)
        logger.debug('RGB: {}'.format(rgb))
        rgb_w = self.xyz_to_rgb(xyz_w)
        logger.debug('RGB_W: {}'.format(rgb_w))
        y_w = xyz_w[1]
        y_b = xyz_b[1]

        h_rgb = 3 * rgb_w / (rgb_w.sum())
        logger.debug('H_RGB: {}'.format(h_rgb))

        # Chromatic adaptation factors
        if not discount_illuminant:
            f_rgb = (1 + (l_a ** (1 / 3)) + h_rgb) / (1 + (l_a ** (1 / 3)) + (1 / h_rgb))
        else:
            f_rgb = numpy.ones(numpy.shape(h_rgb))
        logger.debug('F_RGB: {}'.format(f_rgb))

        # Adaptation factor
        if helson_judd:
            d_rgb = self._f_n((y_b / y_w) * f_l * f_rgb[1]) - self._f_n((y_b / y_w) * f_l * f_rgb)
            assert d_rgb[1] == 0
        else:
            d_rgb = numpy.zeros(numpy.shape(f_rgb))
        logger.debug('D_RGB: {}'.format(d_rgb))

        # Cone bleaching factors
        rgb_b = (10 ** 7) / ((10 ** 7) + 5 * l_a * (rgb_w / 100))
        logger.debug('B_RGB: {}'.format(rgb_b))

        if xyz_p is not None and p is not None:
            logger.debug('Account for simultaneous chromatic contrast')
            rgb_p = self.xyz_to_rgb(xyz_p)
            rgb_w = self.adjust_white_for_scc(rgb_p, rgb_b, rgb_w, p)

        # Adapt rgb using modified
        rgb_a = 1 + rgb_b * (self._f_n(f_l * f_rgb * rgb / rgb_w) + d_rgb)
        logger.debug('RGB_A: {}'.format(rgb_a))

        return rgb_a

    @classmethod
    def adjust_white_for_scc(cls, rgb_p, rgb_b, rgb_w, p):
        """
        Adjust the white point for simultaneous chromatic contrast.

        :param rgb_p: Cone signals of proxima field.
        :param rgb_b: Cone signals of background.
        :param rgb_w: Cone signals of reference white.
        :param p: Simultaneous contrast/assimilation parameter.
        :return: Adjusted cone signals for reference white.
        """
        p_rgb = rgb_p / rgb_b
        rgb_w = rgb_w * (((1 - p) * p_rgb + (1 + p) / p_rgb) ** 0.5) / (((1 + p) * p_rgb + (1 - p) / p_rgb) ** 0.5)
        return rgb_w

    @staticmethod
    def _get_cct(x, y, z):
        """
        Reference
        Hernandez-Andres, J., Lee, R. L., & Romero, J. (1999).
        Calculating correlated color temperatures across the entire gamut of daylight and skylight chromaticities.
        Applied Optics, 38(27), 5703-5709.
        """
        x_e = 0.3320
        y_e = 0.1858

        n = ((x / (x + z + z)) - x_e) / ((y / (x + z + z)) - y_e)

        a_0 = -949.86315
        a_1 = 6253.80338
        a_2 = 28.70599
        a_3 = 0.00004

        t_1 = 0.92159
        t_2 = 0.20039
        t_3 = 0.07125

        cct = a_0 + a_1 * numpy.exp(-n / t_1) + a_2 * numpy.exp(-n / t_2) + a_3 * numpy.exp(-n / t_3)
        return cct

    @staticmethod
    def calculate_scotopic_luminance(photopic_luminance, color_temperature):
        return 2.26 * photopic_luminance * ((color_temperature / 4000) - 0.4) ** (1 / 3)

    @classmethod
    def _calculate_achromatic_signal(cls, l_as, s, s_w, n_bb, a_a):

        j = 0.00001 / ((5 * l_as / 2.26) + 0.00001)
        logger.debug('j: {}'.format(j))

        f_ls = 3800 * (j ** 2) * (5 * l_as / 2.26)
        f_ls += 0.2 * ((1 - (j ** 2)) ** 0.4) * ((5 * l_as / 2.26) ** (1 / 6))
        logger.debug('F_LS: {}'.format(f_ls))

        b_s = 0.5 / (1 + 0.3 * ((5 * l_as / 2.26) * (s / s_w)) ** 0.3)
        b_s += 0.5 / (1 + 5 * (5 * l_as / 2.26))
        logger.debug('B_S: {}'.format(b_s))

        a_s = (cls._f_n(f_ls * s / s_w) * 3.05 * b_s) + 0.3
        logger.debug('A_S: {}'.format(a_s))

        return n_bb * (a_a - 1 + a_s - 0.3 + numpy.sqrt((1 + (0.3 ** 2))))

    @staticmethod
    def _f_n(i):
        """
        Nonlinear response function.
        """
        return 40 * ((i ** 0.73) / (i ** 0.73 + 2))

    @staticmethod
    def _calculate_eccentricity_factor(hue_angle):
        h = numpy.array([20.14, 90, 164.25, 237.53])
        e = numpy.array([0.8, 0.7, 1.0, 1.2])

        out = numpy.interp(hue_angle, h, e)
        out = numpy.where(hue_angle < 20.14, 0.856 - (hue_angle / 20.14) * 0.056, out)
        out = numpy.where(hue_angle > 237.53, 0.856 + 0.344 * (360 - hue_angle) / (360 - 237.53), out)

        return out


class RLAB(object):
    """
    **References**

    * Fairchild, M. D. (1996). Refinement of the RLAB color space. *Color Research & Application*, 21(5), 338-346.
    * Fairchild, M. D. (2013). *Color appearance models*, 3rd Ed. John Wiley & Sons.

    """

    @property
    def hue_angle(self):
        """
        Predicted hue angle :math:`h^R`.
        """
        return self._hue_angle

    @property
    def chroma(self):
        """
        Predicted chroma :math:`C^R`.
        """
        return self._chroma

    @property
    def saturation(self):
        """
        Predicted saturation :math:`s^R`.
        """
        return self._saturation

    @property
    def lightness(self):
        """
        Predicted colorfulness :math:`L^R`.
        """
        return self._lightness

    @property
    def a(self):
        """
        Predicted red-green chromatic response :math:`a^R`.
        """
        return self._a

    @property
    def b(self):
        """
        Predicted yellow-blue chromatic response :math:`b^R`.
        """
        return self._b

    R = numpy.array([[1.9569, -1.1882, 0.2313],
                     [0.3612, 0.6388, 0],
                     [0, 0, 1]])

    def __init__(self, x, y, z, x_n, y_n, z_n, y_n_abs, sigma, d):
        """
        :param x: X value of test sample :math:`X`.
        :param y: Y value of test sample :math:`Y`.
        :param z: Z value of test sample :math:`Z`.
        :param x_n: X value of reference white :math:`X_n`.
        :param y_n: Y value of reference white :math:`Y_n`.
        :param z_n: Z value of reference white :math:`Z_n`.
        :param y_n_abs: Absolute luminance :math:`Y_n` of a white object in cd/m^2.
        :param sigma: Relative luminance parameter :math:`\sigma`. For average surround set :math:`\sigma=1/2.3`,
                      for dim surround :math:`\sigma=1/2.9` and for dark surround :math:`\sigma=1/3.5`.
        :param d: Degree of adaptation :math:`D`.
        """
        xyz = numpy.array([x, y, z])
        xyz_n = numpy.array([x_n, y_n, z_n])

        lms = Hunt.xyz_to_rgb(xyz)
        lms_n = Hunt.xyz_to_rgb(xyz_n)
        logger.debug('LMS: {}'.format(lms))
        logger.debug('LMS_n: {}'.format(lms_n))

        lms_e = (3 * lms_n) / (lms_n[0] + lms_n[1] + lms_n[2])
        lms_p = (1 + (y_n_abs ** (1 / 3)) + lms_e) / (
            1 + (y_n_abs ** (1 / 3)) + (1 / lms_e))
        logger.debug('LMS_e: {}'.format(lms_e))
        logger.debug('LMS_p: {}'.format(lms_p))

        lms_a = (lms_p + d * (1 - lms_p)) / lms_n
        logger.debug('LMS_a: {}'.format(lms_a))

        # If we want to allow arrays as input we need special handling here.
        if len(numpy.shape(x)) == 0:
            # Okay so just a number, we can do things by the book.
            a = numpy.diag(lms_a)
            logger.debug('A: {}'.format(a))
            xyz_ref = self.R.dot(a).dot(Hunt.xyz_to_rgb_m).dot(xyz)
        else:
            # So we have an array. Since constructing huge multidimensional
            # arrays might not bee the best idea, we will handle each input
            # dimension separately. First figure out how many values we have to
            # deal with.
            input_dim = len(x)
            # No create the ouput array that we will fill layer by layer
            xyz_ref = numpy.zeros((3, input_dim))
            for layer in range(input_dim):
                a = numpy.diag(lms_a[..., layer])
                logger.debug('A layer {}: {}'.format(layer, a))
                xyz_ref[..., layer] = self.R.dot(a).dot(Hunt.xyz_to_rgb_m).dot(xyz[..., layer])

        logger.debug('XYZ_ref: {}'.format(xyz_ref))
        x_ref, y_ref, z_ref = xyz_ref

        # Lightness
        self._lightness = 100 * (y_ref ** sigma)
        logger.debug('lightness: {}'.format(self.lightness))

        # Opponent Color Dimensions
        self._a = 430 * ((x_ref ** sigma) - (y_ref ** sigma))
        self._b = 170 * ((y_ref ** sigma) - (z_ref ** sigma))
        logger.debug('a: {}'.format(self._a))
        logger.debug('b: {}'.format(self._b))

        # Hue
        self._hue_angle = (360 * numpy.arctan2(self._b, self._a) / (2 * numpy.pi) + 360) % 360

        # Chroma
        self._chroma = numpy.sqrt((self._a ** 2) + (self._b ** 2))

        # Saturation
        self._saturation = self.chroma / self.lightness


class ATD95(object):
    """
    **References**


    * Fairchild, M. D. (2013). *Color appearance models*, 3rd Ed. John Wiley & Sons.
    * Guth, S. L. (1995, April). Further applications of the ATD model for color vision. In *IS&T/SPIE's Symposium
      on Electronic Imaging: Science & Technology* (pp. 12-26). International Society for Optics and Photonics.

    """

    @property
    def hue(self):
        """
        Predicted hue :math:`H`.
        """
        return self._hue

    @property
    def brightness(self):
        """
        Predicted brightness :math:`Br`.
        """
        return self._brightness

    @property
    def saturation(self):
        """
        Predicted saturation :math:`C`.
        """
        return self._saturation

    def __init__(self, x, y, z, x_0, y_0, z_0, y_0_abs, k_1, k_2, sigma=300):
        """
        :param x: X value of test sample :math:`X`.
        :param y: Y value of test sample :math:`Y`.
        :param z: Z value of test sample :math:`Z`.
        :param x_0: X value of reference white :math:`X_0`.
        :param y_0: Y value of reference white :math:`Y_0`.
        :param z_0: Z value of reference white :math:`Z_0`.
        :param y_0_abs: Absolute adapting luminance :math:`Y_0` in cd/m^2.
        :param k_1: :math:`k_1`
        :param k_2: :math:`k_2`
        :param sigma: :math:`\sigma`
        """
        xyz = self._scale_to_luminance(numpy.array([x, y, z]), y_0_abs)
        xyz_0 = self._scale_to_luminance(numpy.array([x_0, y_0, z_0]), y_0_abs)
        logger.debug('Scaled XYZ: {}'.format(xyz))
        logger.debug('Scaled XYZ_0: {}'.format(xyz))

        # Adaptation Model
        lms = self._xyz_to_lms(xyz)
        logger.debug('LMS: {}'.format(lms))

        xyz_a = k_1 * xyz + k_2 * xyz_0
        logger.debug('XYZ_a: {}'.format(xyz_a))

        lms_a = self._xyz_to_lms(xyz_a)
        logger.debug('LMS_a: {}'.format(lms_a))

        l_g, m_g, s_g = lms * (sigma / (sigma + lms_a))

        # Opponent Color Dimensions
        a_1i = 3.57 * l_g + 2.64 * m_g
        t_1i = 7.18 * l_g - 6.21 * m_g
        d_1i = -0.7 * l_g + 0.085 * m_g + s_g
        a_2i = 0.09 * a_1i
        t_2i = 0.43 * t_1i + 0.76 * d_1i
        d_2i = d_1i

        self._a_1 = self._calculate_final_response(a_1i)
        self._t_1 = self._calculate_final_response(t_1i)
        self._d_1 = self._calculate_final_response(d_1i)
        self._a_2 = self._calculate_final_response(a_2i)
        self._t_2 = self._calculate_final_response(t_2i)
        self._d_2 = self._calculate_final_response(d_2i)

        # Perceptual Correlates
        self._brightness = (self._a_1 ** 2 + self._t_1 ** 2 + self._d_1 ** 2) ** 0.5
        self._saturation = (self._t_2 ** 2 + self._d_2 ** 2) ** 0.5 / self._a_2
        self._hue = self._t_2 / self._d_2

    @staticmethod
    def _calculate_final_response(value):
        return value / (200 + abs(value))

    @staticmethod
    def _scale_to_luminance(xyz, absolute_adapting_luminance):
        return 18 * (absolute_adapting_luminance * xyz / 100) ** 0.8

    @staticmethod
    def _xyz_to_lms(xyz):
        x, y, z = xyz
        l = ((0.66 * (0.2435 * x + 0.8524 * y - 0.0516 * z)) ** 0.7) + 0.024
        m = ((-0.3954 * x + 1.1642 * y + 0.0837 * z) ** 0.7) + 0.036
        s = ((0.43 * (0.04 * y + 0.6225 * z)) ** 0.7) + 0.31
        return numpy.array([l, m, s])


class LLAB(object):
    """
    **References**

    * Fairchild, M. D. (2013). *Color appearance models*, 3rd Ed. John Wiley & Sons.
    * Luo, M. R., & Morovic, J. (1996, September). Two unsolved issues in colour management-colour appearance and
      gamut mapping. In *5th International Conference on High Technology* (pp. 136-147).
    * Luo, M. R., Lo, M. C., & Kuo, W. G. (1996). The LLAB (l: c) colour model.
      *Color Research & Application*, 21(6), 412-429.
    """

    @property
    def hue_angle(self):
        """
        Predicted hue angle :math:`h_L`.
        """
        return self._hue_angle

    @property
    def chroma(self):
        """
        Predicted chroma :math:`Ch_L`.
        """
        return self._chroma

    @property
    def saturation(self):
        """
        Predicted saturation :math:`s_L`.
        """
        return self._saturation

    @property
    def lightness(self):
        """
        Predicted colorfulness :math:`L_L`.
        """
        return self._lightness

    @property
    def a_l(self):
        """
        Predicted red-green chromatic response :math:`A_L`.
        """
        return self._a_l

    @property
    def b_l(self):
        """
        Predicted yellow-blue chromatic response :math:`B_L`.
        """
        return self._b_l

    def __init__(self, x, y, z, x_0, y_0, z_0, y_b, f_s, f_l, f_c, l, d=1):
        """
        :param x: X value of test sample :math:`X`.
        :param y: Y value of test sample :math:`Y`.
        :param z: Z value of test sample :math:`Z`.
        :param x_0: X value of reference white :math:`X_0`.
        :param y_0: Y value of reference white :math:`Y_0`.
        :param z_0: Z value of reference white :math:`Z_0`. 
        :param y_b: Luminance factor of the background :math:`Y_b` in cd/m^2.
        :param f_s: Surround induction factor :math:`F_S`.
        :param f_l: Lightness induction factor :math:`F_L`.
        :param f_c: Chroma induction factor :math:`F_C`.
        :param l: Absolute luminance of reference white :math:`L` in cd/m^2.
        :param d: Discounting-the-Illuminant factor :math:`D`.
        """
        xyz = numpy.array([x, y, z])
        logger.debug('XYZ: {}'.format([x, y, z]))
        xyz_0 = numpy.array([x_0, y_0, z_0])

        r, g, b = self.xyz_to_rgb(xyz)
        logger.debug('RGB: {}'.format([r, g, b]))
        r_0, g_0, b_0 = self.xyz_to_rgb(xyz_0)
        logger.debug('RGB_0: {}'.format([r_0, g_0, b_0]))

        xyz_0r = numpy.array([95.05, 100, 108.88])
        r_0r, g_0r, b_0r = self.xyz_to_rgb(xyz_0r)
        logger.debug('RGB_0r: {}'.format([r_0r, g_0r, b_0r]))

        beta = (b_0 / b_0r) ** 0.0834
        logger.debug('beta: {}'.format(beta))
        r_r = (d * (r_0r / r_0) + 1 - d) * r
        g_r = (d * (g_0r / g_0) + 1 - d) * g
        b_r = (d * (b_0r / (b_0 ** beta)) + 1 - d) * (abs(b) ** beta)
        logger.debug('RGB_r: {}'.format([r_r, g_r, b_r]))

        rgb_r = numpy.array([r_r, g_r, b_r])

        # m_inv = numpy.linalg.inv(self.xyz_to_rgb_m)
        m_inv = numpy.array([[0.987, -0.1471, 0.16],
                             [0.4323, 0.5184, 0.0493],
                             [-0.0085, 0.04, 0.9685]])
        x_r, y_r, z_r = m_inv.dot(rgb_r * y)
        logger.debug('XYZ_r: {}'.format([x_r, y_r, z_r]))

        # Opponent Color Dimension
        def f(w):
            return numpy.where(w > 0.008856,
                               w ** (1 / f_s),
                               (((0.008856 ** (1 / f_s)) - (16 / 116)) / 0.008856) * w + (16 / 116))

        # lightness_contrast_exponent
        z = 1 + f_l * ((y_b / 100) ** 0.5)
        logger.debug('z: {}'.format(z))

        self._lightness = 116 * (f(y_r / 100) ** z) - 16
        a = 500 * (f(x_r / 95.05) - f(y_r / 100))
        b = 200 * (f(y_r / 100) - f(z_r / 108.88))
        logger.debug('A: {}'.format(a))
        logger.debug('B: {}'.format(b))

        logger.debug('f(Xr): {}'.format(f(x_r / 95.05)))
        logger.debug('f(Yr): {}'.format(f(y_r / 100)))
        logger.debug('f(Zr): {}'.format(f(z_r / 108.88)))

        # Perceptual Correlates
        c = (a ** 2 + b ** 2) ** 0.5
        self._chroma = 25 * numpy.log(1 + 0.05 * c)

        s_c = 1 + 0.47 * numpy.log10(l) - 0.057 * numpy.log10(l) ** 2
        s_m = 0.7 + 0.02 * self._lightness - 0.0002 * self._lightness ** 2
        c_l = self._chroma * s_m * s_c * f_c

        self._saturation = self._chroma / self._lightness

        hue_angle_rad = numpy.arctan2(b, a)
        self._hue_angle = hue_angle_rad * 360 / (2 * numpy.pi) % 360

        self._a_l = c_l * numpy.cos(hue_angle_rad)
        self._b_l = c_l * numpy.sin(hue_angle_rad)

    xyz_to_rgb_m = numpy.array([[0.8951, 0.2664, -0.1614],
                                [-0.7502, 1.7135, 0.0367],
                                [0.0389, -0.0685, 1.0296]])

    @classmethod
    def xyz_to_rgb(cls, xyz):
        return cls.xyz_to_rgb_m.dot(xyz / xyz[1])


class CIECAM02(object):
    """
    **References**

    * CIE TC 8-01 (2004). A Color appearance model for color management systems.
      Publication 159. Vienna: CIE Central Bureau. ISBN 3-901906-29-0.
    * Fairchild, M. D. (2013). *Color appearance models*, 3rd Ed. John Wiley & Sons.
    """

    @property
    def hue_angle(self):
        """
        Predicted hue angle :math:`h`.
        """
        return self._h

    @property
    def chroma(self):
        """
        Predicted chroma :math:`C`.
        """
        return self._chroma

    @property
    def saturation(self):
        """
        Predicted saturation :math:`s_L`.
        """
        return self._saturation

    @property
    def lightness(self):
        """
        Predicted colorfulness :math:`J`.
        """
        return self._lightness

    @property
    def brightness(self):
        """
        Predicted colorfulness :math:`Q`.
        """
        return self._brightness

    @property
    def colorfulness(self):
        """
        Predicted colorfulness :math:`M`.
        """
        return self._colorfulness

    @property
    def a(self):
        """
        Predicted red-green chromatic response :math:`a`.
        """
        return self._a

    @property
    def b(self):
        """
        Predicted yellow-blue chromatic response :math:`b`.
        """
        return self._b

    M_CAT02 = numpy.array([[0.7328, 0.4296, -0.1624],
                           [-0.7036, 1.6975, 0.0061],
                           [0.0030, 0.0136, 0.9834]])

    M_CAT02_inv = numpy.linalg.inv(M_CAT02)

    M_HPE = numpy.array([[0.38971, 0.68898, -0.07868],
                         [-0.22981, 1.18340, 0.04641],
                         [0, 0, 1]])

    def __init__(self, x, y, z, x_w, y_w, z_w, y_b, l_a, c, n_c, f, d=False):
        """
        :param x: X value of test sample :math:`X`.
        :param y: Y value of test sample :math:`Y`.
        :param z: Z value of test sample :math:`Z`.
        :param x_w: X value of reference white :math:`X_W`.
        :param y_w: Y value of reference white :math:`Y_W`.
        :param z_w: Z value of reference white :math:`Z_W`.
        :param y_b: Background relative luminance :math:`Y_b`.
        :param l_a: Adapting luminance :math:`L_A` in cd/m^2.
        :param c: Exponential nonlinearity :math:`c`. (Average/Dim/Dark) (0.69/0.59/0.525).
        :param n_c: Chromatic induction factor :math:`N_c`. (Average/Dim/Dark) (1.0,0.9,0.8).
        :param f: Maximum degree of adaptation :math:`F`. (Average/Dim/Dark) (1.0/0.9/0.8).
        :param d: Discount-the-Illuminant factor :math:`D`.
        """

        xyz = numpy.array([x, y, z])
        xyz_w = numpy.array([x_w, y_w, z_w])

        # Determine the degree of adaptation
        if not d:
            d = self._compute_degree_of_adaptation(f, l_a)
        else:
            d = 1
        logger.debug("D: {}".format(d))

        # Compute viewing condition dependant components
        k = 1 / (5 * l_a + 1)
        logger.debug("k: {}".format(k))

        f_l = 0.2 * (k ** 4) * 5 * l_a + 0.1 * (1 - k ** 4) ** 2 * (5 * l_a) ** (1 / 3)
        logger.debug("F_L: {}".format(f_l))
        n = y_b / y_w
        logger.debug("n: {}".format(n))
        self.n_bb = self.n_cb = 0.725 * n ** -0.2
        z = 1.48 + numpy.sqrt(n)
        logger.debug("z".format(z))

        rgb_a, rgb_aw = self._compute_adaptation(xyz, xyz_w, f_l, d)
        logger.debug("RGB'a: {}".format(rgb_a))
        logger.debug("RGB'aw: {}".format(rgb_aw))

        r_a, g_a, b_a = rgb_a
        r_aw, g_aw, b_aw = rgb_aw

        # Opponent Color Dimensions
        self._a = r_a - 12 * g_a / 11 + b_a / 11
        self._b = (1 / 9) * (r_a + g_a - 2 * b_a)

        # Hue
        self._h = 360 * numpy.arctan2(self._b, self._a) / (2 * numpy.pi)
        e_t = (1 / 4) * (numpy.cos(2 + self._h * numpy.pi / 180) + 3.8)

        # Lightness
        a = self._compute_achromatic_response(r_a, g_a, b_a, self.n_bb)
        logger.debug('A: {}'.format(a))
        a_w = self._compute_achromatic_response(r_aw, g_aw, b_aw, self.n_bb)
        logger.debug('A_W: {}'.format(a_w))
        self._lightness = 100 * (a / a_w) ** (c * z)  # 16.24

        # Brightness
        # self._brightness = self.compute_brightness(self.lightness, surround, a_w, f_l)
        self._brightness = (4 / c) * numpy.sqrt(self._lightness / 100) * (a_w + 4) * f_l ** 0.25

        # Chroma
        # self.chroma = self.compute_chroma(rgb_a, self.lightness, surround, self.N_cb, e_t, self.a, self.b, n)
        t = ((50000 / 13) * n_c * self.n_cb * e_t * numpy.sqrt((self._a ** 2) + (self._b ** 2))) / (
            rgb_a[0] + rgb_a[1] + (21 / 20) * rgb_a[2])
        self._chroma = (t ** 0.9) * numpy.sqrt(self._lightness / 100) * ((1.64 - 0.29 ** n) ** 0.73)

        # Colorfulness
        self._colorfulness = self.chroma * f_l ** 0.25

        # Saturation
        self._saturation = 100 * numpy.sqrt(self._colorfulness / self._brightness)

        # Cartesian coordinates
        self.a_c, self.b_c = self._compute_cartesian_coordinates(self.chroma, self._h)
        self.a_m, self.b_m = self._compute_cartesian_coordinates(self._colorfulness, self._h)
        self.a_s, self.b_s = self._compute_cartesian_coordinates(self.saturation, self._h)

    @classmethod
    def _compute_adaptation(cls, xyz, xyz_w, f_l, d):
        # Transform input colors to cone responses
        rgb = cls._xyz_to_rgb(xyz)
        logger.debug("RGB: {}".format(rgb))
        rgb_w = cls._xyz_to_rgb(xyz_w)
        logger.debug("RGB_W: {}".format(rgb_w))

        # Compute adapted tristimulus-responses
        rgb_c = cls._white_adaption(rgb, rgb_w, d)
        logger.debug("RGB_C: {}".format(rgb_c))
        rgb_cw = cls._white_adaption(rgb_w, rgb_w, d)
        logger.debug("RGB_CW: {}".format(rgb_cw))

        # Convert adapted tristimulus-responses to Hunt-Pointer-Estevez fundamentals
        rgb_p = cls._compute_hunt_pointer_estevez_fundamentals(rgb_c)
        logger.debug("RGB': {}".format(rgb_p))
        rgb_wp = cls._compute_hunt_pointer_estevez_fundamentals(rgb_cw)
        logger.debug("RGB'_W: {}".format(rgb_wp))

        # Compute post-adaptation non-linearities
        rgb_ap = cls._compute_nonlinearities(f_l, rgb_p)
        rgb_awp = cls._compute_nonlinearities(f_l, rgb_wp)

        return rgb_ap, rgb_awp

    @staticmethod
    def _xyz_to_rgb(xyz):
        return numpy.dot(CIECAM02.M_CAT02, xyz)

    @staticmethod
    def _rgb_to_xyz(rgb):
        return numpy.dot(CIECAM02.M_CAT02_inv, rgb)

    @staticmethod
    def _white_adaption(rgb, rgb_w, d=1):
        return ((100 * d / rgb_w) + (1 - d)) * rgb

    @staticmethod
    def _compute_degree_of_adaptation(surround_conditions, adapting_luminance):
        return surround_conditions * (1 - (1 / 3.6) * numpy.exp((-adapting_luminance - 42) / 92))

    @staticmethod
    def _compute_hunt_pointer_estevez_fundamentals(rgb):
        return numpy.dot(numpy.dot(CIECAM02.M_HPE, CIECAM02.M_CAT02_inv), rgb)

    @staticmethod
    def _compute_nonlinearities(f_l, rgb):
        return 0.1 + (400 * (f_l * rgb / 100) ** 0.42) / (27.13 + (f_l * rgb / 100) ** 0.42)

    @staticmethod
    def _compute_achromatic_response(r, g, b, n_bb):
        return (2 * r + g + (1 / 20) * b - 0.305) * n_bb

    @staticmethod
    def _compute_cartesian_coordinates(value, hue):
        a = value * numpy.cos(hue * numpy.pi / 180)  # 16.30
        b = value * numpy.sin(hue * numpy.pi / 180)  # 16.31
        return a, b


class CIECAM02m1(CIECAM02):
    """
    **References**

    * Wu, R. C., & Wardman, R. H. (2007). Proposed modification to the CIECAM02 colour appearance model to include the
      simultaneous contrast effects. *Color Research & Application*, 32(2), 121-129.
    """
    def __init__(self, x, y, z, x_w, y_w, z_w, x_b, y_b, z_b, l_a, c, n_c, f, p, d=False):
        """
        :param x: X value of test sample :math:`X`.
        :param y: Y value of test sample :math:`Y`.
        :param z: Z value of test sample :math:`Z`.
        :param x_w: X value of reference white :math:`X_W`.
        :param y_w: Y value of reference white :math:`Y_W`.
        :param z_w: Z value of reference white :math:`Z_W`.
        :param x_b: X value of background :math:`X_b`.
        :param y_b: Y value of background :math:`Y_b`.
        :param z_b: Z value of background :math:`Z_b`.
        :param l_a: Adapting luminance :math:`L_A` in cd/m^2.
        :param c: Exponential nonlinearity :math:`c`. (Average/Dim/Dark) (0.69/0.59/5.25).
        :param n_c: Chromatic induction factor :math:`N_c`. (Average/Dim/Dark) (1.0,0.9,0.8).
        :param f: Maximum degree of adaptation :math:`F`. (Average/Dim/Dark) (1.0/0.9/0.8).
        :param p: Simultaneous contrast/assimilation parameter.
        :param d: Discount-the-Illuminant factor :math:`D`.
        """

        self._p = p
        self._xyz_b = numpy.array([x_b, y_b, z_b])

        super(CIECAM02m1, self).__init__(x, y, z, x_w, y_w, z_w, y_b, l_a, c, n_c, f, d)

    def _compute_adaptation(self, xyz, xyz_w, f_l, d):
        """
        Modified adaptation procedure incorporating simultaneous chromatic contrast from Hunt model.

        :param xyz: Stimulus XYZ.
        :param xyz_w: Reference white XYZ.
        :param f_l: Luminance adaptation factor
        :param d: Degree of adaptation.
        :return: Tuple of adapted rgb and rgb_w arrays.
        """
        # Transform input colors to cone responses
        rgb = self._xyz_to_rgb(xyz)
        logger.debug("RGB: {}".format(rgb))

        rgb_b = self._xyz_to_rgb(self._xyz_b)
        rgb_w = self._xyz_to_rgb(xyz_w)
        rgb_w = Hunt.adjust_white_for_scc(rgb, rgb_b, rgb_w, self._p)
        logger.debug("RGB_W: {}".format(rgb_w))

        # Compute adapted tristimulus-responses
        rgb_c = self._white_adaption(rgb, rgb_w, d)
        logger.debug("RGB_C: {}".format(rgb_c))
        rgb_cw = self._white_adaption(rgb_w, rgb_w, d)
        logger.debug("RGB_CW: {}".format(rgb_cw))

        # Convert adapted tristimulus-responses to Hunt-Pointer-Estevez fundamentals
        rgb_p = self._compute_hunt_pointer_estevez_fundamentals(rgb_c)
        logger.debug("RGB': {}".format(rgb_p))
        rgb_wp = self._compute_hunt_pointer_estevez_fundamentals(rgb_cw)
        logger.debug("RGB'_W: {}".format(rgb_wp))

        # Compute post-adaptation non-linearities
        rgb_ap = self._compute_nonlinearities(f_l, rgb_p)
        rgb_awp = self._compute_nonlinearities(f_l, rgb_wp)

        return rgb_ap, rgb_awp
