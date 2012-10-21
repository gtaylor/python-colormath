#!/usr/bin/env python
from distutils.core import setup
import colormath

LONG_DESCRIPTION = open('README.rst').read()

CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
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
      license = 'BSD',
      classifiers = CLASSIFIERS,
      keywords = KEYWORDS,
      requires = ['numpy']
     )
