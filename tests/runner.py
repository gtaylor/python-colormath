"""
Master test suite runner. Hit this in the shell to run all of the test suites
in one fell swoop. Make sure these are ran every time 
colormath/color_conversions.py is touched.
"""
import unittest
import conversions

# A list of the modules under the tests package that should be ran.
test_modules = [conversions]

# Fire off all of the tests.
for mod in test_modules:
    suite = unittest.TestLoader().loadTestsFromModule(mod)
    unittest.TextTestRunner(verbosity=2).run(suite)