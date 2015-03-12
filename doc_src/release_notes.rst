.. _release_notes:

.. include:: global.txt

Release Notes
=============

2.1.1
-----

Bug Fixes
^^^^^^^^^

* Add ``network`` to install_requires. (Ed-von-Schleck)

2.1.0
-----

Features
^^^^^^^^

* Added new NetworkX graph-based resolution of conversions between
  color spaces. Reduces boilerplate and makes it much easier to add
  additional color spaces going forward. (MichaelMauderer)
* Added the IPT color space. (MichaelMauderer)
* Added Color Appearance Models. Natayani95, Hunt, RLAB, ATD95, 
  LLAB, CIECAM02, CIECAM02-m1. (MichaelMauderer)

Bug Fixes
^^^^^^^^^

* xyY conversions now correctly avoid division by zero. (dwbullok)
* Un-transposed adaptation matrices. Has no effect on conversions, 
  but if you use these directly you may see different numbers. (JasonTam)
* During XYZ->RGB, linear channel values are now clamped in order to avoid
  domain errors. Output should now always be between 0 and 1.
  
Backwards Incompatible changes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* If any of your code directly referenced the color adaptation matrices
  that were un-inverted, you'll need to adjust your math.

2.0.2
-----

Bug Fixes
^^^^^^^^^

* Apparently I didn't add the function body for the clamped RGB properties.
  Yikes.

2.0.1
-----

Features
^^^^^^^^
* Lots of documentation improvements.
* :py:meth:`convert_color()` now has an explicitly defined/documented
  ``target_illuminant`` kwarg, instead of letting this fall through to its
  **kwargs. This should make IDE auto-complete better and provide more clarity.
* Added ``clamped_rgb_r``, ``clamped_rgb_g``, and ``clamped_rgb_b`` to RGB
  color spaces. Use these if you have to have in-gamut, potentially compressed
  coordinates.

Bug Fixes
^^^^^^^^^
* Direct conversions to non-sRGB colorspaces returned sRGBColor objects.
  Reported by Cezary Wagner.

2.0.0
-----

Backwards Incompatible changes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* Minimum Python version is now 2.7.
* ColorBase.convert_to() is no more. Use colormath.color_conversions.convert_color()
  instead. API isn't as spiffy looking, but it's a lot less magical now.
* Completely re-worked RGB handling. Each RGB space now has its own class,
  inheriting from BaseRGBColor. Consequently, RGBColor is no more. In most
  cases, you can substitute RGBColor with sRGBColor during your upgrade.
* RGB channels are now [0..1] instead of [1..255]. Can use
  BaseRGBColor.get_upscaled_value_tuple() to get the upscaled values.
* BaseRGBColor.set_from_rgb_hex() was replaced with a
  BaseRGBColor.new_from_rgb_hex(), which returns a properly formed sRGBColor object.
* BaseRGBColor no longer accepts observer or illuminant kwargs.
* HSL no longer accepts observer, illuminant or rgb_type kwargs.
* HSV no longer accepts observer, illuminant or rgb_type kwargs.
* CMY no longer accepts observer, illuminant or rgb_type kwargs.
* CMYK no longer accepts observer, illuminant or rgb_type kwargs.
* Removed 'debug' kwargs in favor of Python's logging.
* Completely re-worked exception list. Eliminated some redundant exceptions,
  re-named basically everything else.

Features
^^^^^^^^
* Python 3.3 support added.
* Added tox.ini with supported environments.
* Removed the old custom test runner in favor of nose.
* Replacing simplified RGB->XYZ conversions with Bruce Lindbloom's.
* A round of PEP8 work.
* Added a BaseColorConversionTest test class with some greatly improved
  color comparison. Much more useful in tracking down breakages.
* Eliminated non-matrix delta E computations in favor of the matrix equivalents.
  No need to maintain duplicate code, and the matrix stuff is faster for bulk
  operations.

Bug Fixes
^^^^^^^^^

* Corrected delta_e CMC example error. Should now run correctly.
* color_diff_matrix.delta_e_cie2000 had an edge case where certain angles
  would result in an incorrect delta E.
* Un-hardcoded XYZColor.apply_adaptation()'s adaptation and observer angles.

1.0.9
-----

Features
^^^^^^^^
* Added an optional vectorized deltaE function. This uses NumPy array/matrix
  math for a very large speed boost. (Eddie Bell)
* Added this changelog.

Bug Fixes
^^^^^^^^^
* Un-hardcode the observer angle in adaptation matrix. (Bastien Dejean)

1.0.8
-----

* Initial GitHub release.

