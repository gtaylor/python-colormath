.. _index:

.. include:: global.txt

python-colormath
================

python-colormath is a simple Python module that spares the user from directly
dealing with
`color math <http://www.brucelindbloom.com/index.html?Eqn_DeltaE_CMC.html>`_.
Some features include:

* Support for a wide range of color spaces. A good chunk of the CIE spaces,
  RGB, HSL/HSV, CMY/CMYK, and many more.
* Conversions between the various color spaces. For example, XYZ to sRGB,
  Spectral to XYZ, CIE Lab to Adobe RGB.
* All CIE Delta E functions, plus CMC.
* Chromatic adaptations (changing illuminants).
* RGB to hex and vice-versa.
* 16-bit RGB support.
* Runs on Python 2.7 and Python 3.3.

**License:** python-colormath is licensed under the `BSD License`_.

Assorted Info
-------------

* `Issue tracker`_ - Report bugs here.
* `GitHub project`_ - Source code and issue tracking.
* `@gctaylor Twitter`_ - Tweets from the maintainer.

General Topics
--------------

.. toctree::
   :maxdepth: 2

   installation
   color_objects
   illuminants
   conversions
   delta_e
   density
