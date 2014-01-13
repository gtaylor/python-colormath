"""
Master test suite runner. Hit this in the shell to run all of the test suites
in one fell swoop. Make sure these are ran every time
colormath/color_conversions.py is touched.
"""
import os
import sys
# Prepare the path to use the included colormath directory.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unittest
import t_color_objects
import t_color_diff
import t_color_diff_matrix
import t_chromatic_adaptation
# A list of the modules under the tests package that should be ran.
test_modules = [t_color_objects, t_color_diff, t_color_diff_matrix, t_chromatic_adaptation]

# Fire off all of the tests.
for mod in test_modules:
    suite = unittest.TestLoader().loadTestsFromModule(mod)
    unittest.TextTestRunner(verbosity=1).run(suite)
