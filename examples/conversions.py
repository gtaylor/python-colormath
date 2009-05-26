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
This module shows you how to perform color space conversions. Please see the
chart on www.brucelindbloom.com/Math.html for an illustration of the conversions
you may perform.
"""
from colormath.color_objects import LabColor, LCHabColor

def example_lab_to_xyz():
    """
    This function shows a simple conversion of an Lab color to an XYZ color
    with debugging on (to show verbose output so you can see what the library
    is doing for you).
    """
    print "=== Simple Example: Lab->XYZ ==="
    # Instantiate an Lab color object with the given values.
    lab = LabColor(lab_l = 0.903, lab_a = 16.296, lab_b = -2.22)
    # Show a string representation.
    print lab
    # Convert to XYZ.
    xyz = lab.convert_to('xyz', debug=False)
    print xyz
    print "=== End Example ===\n"
    
def example_lchab_to_lchuv():
    """
    This function shows very complex chain of conversions in action. While this
    requires no additional effort from the user, debugging mode will show you
    all of the work that goes on behind the scenes.
    
    LCHab to LCHuv involves four different calculations, making this the
    conversion requiring the most steps.
    """
    print "=== Complex Example: LCHab->LCHuv ==="
    # Instantiate an LCHab color object with the given values.
    lchab = LCHabColor(lch_l = 0.903, lch_c = 16.447, lch_h = 352.252)
    # Show a string representation.
    print lchab
    # Convert to LCHuv.
    lchuv = lchab.convert_to('lchuv', debug=False)
    print lchuv
    print "=== End Example ===\n"
    
def example_lab_to_rgb():
    """
    Conversions to RGB are a little more complex mathematically. There are also
    several kinds of RGB color spaces. When converting from a device-independent
    color space to RGB, sRGB is assumed unless otherwise specified with the
    target_rgb keyword arg.
    """
    print "=== RGB Example: Lab->RGB ==="
    # Instantiate an Lab color object with the given values.
    lab = LabColor(lab_l = 0.903, lab_a = 16.296, lab_b = -2.217)
    # Show a string representation.
    print lab
    # Convert to XYZ.
    rgb = lab.convert_to('rgb', target_rgb='sRGB', debug=False)
    print rgb
    print "=== End Example ===\n"
    
# Feel free to comment/un-comment examples as you please.
example_lab_to_xyz()
example_lchab_to_lchuv()
example_lab_to_rgb()