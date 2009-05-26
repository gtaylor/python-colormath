"""
Master test suite runner. Hit this in the shell to run all of the test suites
in one fell swoop. Make sure these are ran every time 
colormath/color_conversions.py is touched.
"""
import unittest
import t_color_objects

# A list of the modules under the tests package that should be ran.
test_modules = [t_color_objects]

# Fire off all of the tests.
for mod in test_modules:
    suite = unittest.TestLoader().loadTestsFromModule(mod)
    unittest.TextTestRunner(verbosity=1).run(suite)