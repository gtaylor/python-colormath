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
This module shows you how to perform various kinds of density calculations.
"""
import example_config
from colormath.color_objects import SpectralColor
from colormath.density_standards import *

EXAMPLE_COLOR = SpectralColor(observer=2, illuminant='d50', 
                    spec_380nm=0.0600, spec_390nm=0.0600, spec_400nm=0.0641,
                    spec_410nm=0.0654, spec_420nm=0.0645, spec_430nm=0.0605,
                    spec_440nm=0.0562, spec_450nm=0.0543, spec_460nm=0.0537,
                    spec_470nm=0.0541, spec_480nm=0.0559, spec_490nm=0.0603,
                    spec_500nm=0.0651, spec_510nm=0.0680, spec_520nm=0.0705,
                    spec_530nm=0.0736, spec_540nm=0.0772, spec_550nm=0.0809,
                    spec_560nm=0.0870, spec_570nm=0.0990, spec_580nm=0.1128,
                    spec_590nm=0.1251, spec_600nm=0.1360, spec_610nm=0.1439,
                    spec_620nm=0.1511, spec_630nm=0.1590, spec_640nm=0.1688,
                    spec_650nm=0.1828, spec_660nm=0.1996, spec_670nm=0.2187,
                    spec_680nm=0.2397, spec_690nm=0.2618, spec_700nm=0.2852,
                    spec_710nm=0.2500, spec_720nm=0.2400, spec_730nm=0.2300)

def example_auto_status_t_density():
    print "=== Example: Automatic Status T Density ==="
    # If no arguments are provided to calc_density(), ANSI Status T density is
    # assumed. The correct RGB "filter" is automatically selected for you.
    print "Density: %f" % EXAMPLE_COLOR.calc_density()
    print "=== End Example ===\n"
    
def example_manual_status_t_density():
    print "=== Example: Manual Status T Density ==="
    # Here we are specifically requesting the value of the red band via the
    # ANSI Status T spec.
    print "Density: %f (Red)" % EXAMPLE_COLOR.calc_density(density_standard=ANSI_STATUS_T_RED)
    print "=== End Example ===\n"
    
def example_visual_density():
    print "=== Example: Visual Density ==="
    # Here we pass the ISO Visual spectral standard.
    print "Density: %f" % EXAMPLE_COLOR.calc_density(density_standard=ISO_VISUAL)
    print "=== End Example ===\n"
    
# Feel free to comment/un-comment examples as you please.
example_auto_status_t_density()
example_manual_status_t_density()
example_visual_density()
