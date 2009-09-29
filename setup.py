#!/usr/bin/env python
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
from distutils.core import setup
import colormath

LONG_DESCRIPTION = \
"""Implements a large number of different color operations such as
color space conversions, Delta E, and density to spectral."""

CLASSIFIERS = [
                'Development Status :: 5 - Production/Stable',
                'Intended Audience :: Developers',
                'License :: OSI Approved :: GNU General Public License (GPL)',
                'Natural Language :: English',
                'Operating System :: OS Independent',
                'Programming Language :: Python',
                'Topic :: Scientific/Engineering :: Mathematics',
                'Topic :: Software Development :: Libraries :: Python Modules' 
              ]

KEYWORDS = 'color math conversions'

setup(name='colormath',
      version=colormath.VERSION,
      description='Color math and conversion library.',
      long_description = LONG_DESCRIPTION,
      author='Gregory Taylor',
      author_email='gtaylor@l11solutions.com',
      url='http://code.google.com/p/python-colormath/',
      download_url='http://pypi.python.org/pypi/colormath/',
      packages=['colormath'],
      platforms = ['Platform Independent'],
      license = 'GPLv3',
      classifiers = CLASSIFIERS,
      keywords = KEYWORDS,
      requires = ['numpy']
     )
