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

from abc import abstractmethod
from collections import defaultdict
import csv
import os

import unittest
import numpy

from numpy.testing import assert_allclose, assert_almost_equal
from colormath.color_appearance_models import CIECAM02, RLAB, LLAB, ATD95, Nayatani95, Hunt


class ColorAppearanceTest():
    fixture_path = None

    @staticmethod
    def load_fixture(file_name):
        path = os.path.dirname(__file__)
        with open(os.path.join(path, 'fixtures', file_name)) as in_file:
            result = []
            for case_data in csv.DictReader(in_file):
                for key in case_data:
                    try:
                        case_data[key] = float(case_data[key])
                    except ValueError:
                        pass
                result.append(case_data)
            return result

    def check_model_consistency(self, data, output_parameter_dict):
        for data_attr, model_attr in sorted(output_parameter_dict.items()):
            yield self.check_model_attribute, data.get('Case'), data, model_attr, data[data_attr]

    @abstractmethod
    def create_model_from_data(self, data):
        pass

    def check_model_attribute(self, case, data, model_attr, target):
        model = self.create_model_from_data(data)
        model_parameter = getattr(model, model_attr)
        error_message = 'Parameter {} in test case {} does not match target value.\nExpected: {} \nReceived {}'.format(
            model_attr, case, target, model_parameter)

        assert_allclose(model_parameter, target, err_msg=error_message, rtol=0.01, atol=0.01, verbose=False)
        assert_almost_equal(model_parameter, target, decimal=1, err_msg=error_message)

    limited_fixtures = None

    def _get_fixtures(self):
        # Sometimes it might be desirable to exclude s specific fixture for testing
        fixtures = self.load_fixture(self.fixture_path)
        if self.limited_fixtures is not None:
            fixtures = [fixtures[index] for index in self.limited_fixtures]
        return fixtures

    def test_forward_examples(self):
        # Go through all available fixtures
        for data in self._get_fixtures():
            # Create a single test for each output parameter
            for test in self.check_model_consistency(data, self.output_parameter_dict):
                yield test

    def test_parallel_forward_example(self):
        # Collect all fixture data in a single dict of lists
        data = defaultdict(list)
        for fixture in self._get_fixtures():
            for key, value in fixture.items():
                data[key].append(value)
        # Turn lists into numpy.arrays
        for key in data:
            data[key] = numpy.array(data[key])
        # Create tests
        for test in self.check_model_consistency(data, self.output_parameter_dict):
            yield test


class TestNayataniColorAppearanceModel(ColorAppearanceTest):
    fixture_path = 'nayatani.csv'

    output_parameter_dict = {'L_star_P': '_lightness_achromatic',
                             'L_star_N': '_lightness_achromatic_normalized',
                             'theta': 'hue_angle',
                             'C': 'chroma',
                             'S': 'saturation',
                             'B_r': 'brightness',
                             'M': 'colorfulness'}

    def create_model_from_data(self, data):
        model = Nayatani95(data['X'], data['Y'], data['Z'],
                           data['X_n'], data['Y_n'], data['Z_n'],
                           data['Y_o'],
                           data['E_o'],
                           data['E_or'])
        return model

    @staticmethod
    def test_beta_1():
        assert_almost_equal(Nayatani95._beta_1(0), 1, decimal=6)
        assert_almost_equal(Nayatani95._beta_1(1), 1.717900656, decimal=6)
        assert_almost_equal(Nayatani95._beta_1(2), 1.934597896, decimal=6)

    @staticmethod
    def test_beta_2():
        assert_almost_equal(Nayatani95._beta_2(0), 0.7844, decimal=6)
        assert_almost_equal(Nayatani95._beta_2(1), 1.375241343, decimal=6)
        assert_almost_equal(Nayatani95._beta_2(2), 1.59085866, decimal=6)


class TestHuntColorAppearanceModel(ColorAppearanceTest):
    fixture_path = 'hunt.csv'

    output_parameter_dict = {'h_S': 'hue_angle',
                             's': 'saturation',
                             'Q': 'brightness',
                             'J': 'lightness',
                             'C_94': 'chroma',
                             'M94': 'colorfulness'}

    def create_model_from_data(self, data):
        model = Hunt(data['X'], data['Y'], data['Z'],
                     data['X_W'], 0.2 * data['Y_W'], data['Z_W'],
                     data['X_W'], data['Y_W'], data['Z_W'],
                     l_a=data['L_A'],
                     n_c=data['N_c'],
                     n_b=data['N_b'],
                     cct_w=data['T'])

        return model


class TestRLABColorAppearanceModel(ColorAppearanceTest):
    fixture_path = 'rlab.csv'
    output_parameter_dict = {'L': 'lightness',
                             'C': 'chroma',
                             's': 'saturation',
                             'a': 'a',
                             'b': 'b',
                             'h': 'hue_angle'}

    def create_model_from_data(self, data):
        model = RLAB(data['X'], data['Y'], data['Z'],
                     data['X_n'], data['Y_n'], data['Z_n'],
                     data['Y_n2'],
                     data['sigma'],
                     data['D'])
        return model


class TestATDColorAppearanceModel(ColorAppearanceTest):
    fixture_path = 'atd.csv'

    output_parameter_dict = {'A_1': '_a_1',
                             'T_1': '_t_1',
                             'D_1': '_d_1',
                             'A_2': '_a_2',
                             'T_2': '_t_2',
                             'D_2': '_d_2',
                             'Br': 'brightness',
                             'C': 'saturation',
                             'H': 'hue'}

    def create_model_from_data(self, data):
        model = ATD95(data['X'], data['Y'], data['Z'],
                      data['X_0'], data['Y_0'], data['Z_0'],
                      data['Y_02'],
                      data['K_1'], data['K_2'],
                      data['sigma'])
        return model

    @staticmethod
    def test_xyz_to_lms():
        l, m, s = ATD95._xyz_to_lms(numpy.array([1, 1, 1]))
        assert_almost_equal(l, 0.7946522478109985)
        assert_almost_equal(m, 0.9303058494144267)
        assert_almost_equal(s, 0.7252006614718631)

    @staticmethod
    def test_final_response_calculation():
        assert_almost_equal(ATD95._calculate_final_response(0), 0)
        assert_almost_equal(ATD95._calculate_final_response(100), 1.0 / 3.0)
        assert_almost_equal(ATD95._calculate_final_response(200), 0.5)
        assert_almost_equal(ATD95._calculate_final_response(10000), 0.980392157)


class TestLLABColorAppearanceModel(ColorAppearanceTest):
    fixture_path = 'llab.csv'

    output_parameter_dict = {'L_L': 'lightness',
                             'Ch_L': 'chroma',
                             's_L': 'saturation',
                             'h_L': 'hue_angle',
                             'A_L': 'a_l',
                             'B_L': 'b_l'}

    def create_model_from_data(self, data):
        model = LLAB(data['X'], data['Y'], data['Z'],
                     data['X_0'], data['Y_0'], data['Z_0'],
                     data['Y_b'],
                     data['F_S'],
                     data['F_L'],
                     data['F_C'],
                     data['L'])
        return model


class TestCIECAM02ColorAppearanceModel(ColorAppearanceTest):
    fixture_path = 'ciecam02.csv'
    output_parameter_dict = {'J': 'lightness',
                             'Q': 'brightness',
                             'C': 'chroma',
                             'M': 'colorfulness',
                             'S': 'saturation',
                             'N_bb': 'n_bb',
                             'a_c': 'a_c',
                             'b_c': 'b_c',
                             'a_M': 'a_m',
                             'b_M': 'b_m',
                             'a_s': 'a_s',
                             'b_s': 'b_s'}

    input_parameter_dict = {}

    def create_model_from_data(self, data):
        model = CIECAM02(data['X'], data['Y'], data['Z'],
                         data['X_W'], data['Y_W'], data['Z_W'],
                         data['Y_b'],
                         data['L_A'],
                         data['c'], data['N_c'], data['F'])
        return model

    @staticmethod
    def test_degree_of_adaptation():
        assert_almost_equal(CIECAM02._compute_degree_of_adaptation(1, 100), 0.940656, decimal=6)
        assert_almost_equal(CIECAM02._compute_degree_of_adaptation(1, 318.31), 0.9994, decimal=2)
        assert_almost_equal(CIECAM02._compute_degree_of_adaptation(1, 31.83), 0.875, decimal=2)

    @staticmethod
    def test_xyz_to_rgb():
        assert_almost_equal(CIECAM02._xyz_to_rgb(numpy.array([95.05, 100, 108.9])),
                            numpy.array([94.9273, 103.527, 108.737]),
                            decimal=2)


@unittest.skip
class TestCIECAM02m1ColorAppearanceModel(ColorAppearanceTest):
    # TODO: Test CIECAM02-m1 model
    pass
