"""
 Color Math Module (colormath) 
 Copyright (C) 2009 Gregory Taylor

 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

"""
Master test suite runner. Hit this in the shell to run all of the test suites
in one fell swoop. Make sure these are ran every time 
colormath/color_conversions.py is touched.
"""
import unittest
import t_color_objects
import t_color_diff
import t_chromatic_adaptation

# A list of the modules under the tests package that should be ran.
test_modules = [t_color_objects, t_color_diff, t_chromatic_adaptation]

# Fire off all of the tests.
for mod in test_modules:
    suite = unittest.TestLoader().loadTestsFromModule(mod)
    unittest.TextTestRunner(verbosity=1).run(suite)