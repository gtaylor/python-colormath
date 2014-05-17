.. _conversions:

.. include:: global.txt

Color Conversions
=================

Converting between color spaces is very simple with python-colormath. To see
a full list of supported color spaces, see :doc:`color_objects`.

All conversions happen through the ``convert_color`` function shown below.
The original Color instance is passed in as the first argument, and the
desired Color class (not an instance) is passed in as the second argument.
If the conversion can be made, a new Color instance will be returned.

.. autofunction:: colormath.color_conversions.convert_color

Example
-------

This is a simple example of a CIE Lab to CIE XYZ conversion. Refer to
:doc:`color_objects` for a full list of different color spaces that can
be instantiated and converted between.

.. code-block:: python

    from colormath.color_objects import LabColor, XYZColor
    from colormath.color_conversions import convert_color

    lab = LabColor(0.903, 16.296, -2.22)
    xyz = convert_color(lab, XYZColor)

Some color spaces require a trip through RGB during conversion. For example,
to get from XYZ to HSL, we have to convert XYZ->RGB->HSL. The same could
be said for XYZ to CMYK (XYZ->RGB->CMY->CMYK). Different RGB color spaces
have different gamut sizes and capabilities, which can affect your
converted color values.

sRGB is the default RGB color space due to its ubiquity. If you would like
to use a different RGB space for a conversion, you can do something like this:

.. code-block:: python

    from colormath.color_objects import XYZColor, HSLColor, AdobeRGBColor
    from colormath.color_conversions import convert_color

    xyz = XYZColor(0.1, 0.2, 0.3)
    hsl = convert_color(xyz, HSLColor, through_rgb_type=AdobeRGBColor)
    # If you are going to convert back to XYZ, make sure you use the same
    # RGB color space on the way back.
    xyz2 = convert_color(hsl, XYZColor, through_rgb_type=AdobeRGBColor)

RGB conversions and native illuminants
--------------------------------------

When converting RGB colors to any of the CIE spaces, we have to pass through
the XYZ color space. This serves as a crossroads for conversions to basically
all of the reflective color spaces (CIE Lab, LCH, Luv, etc). The RGB spaces
are reflective, where the illumination is provided. In the case of a reflective
space like XYZ, the illuminant must be supplied by a light source.

Each RGB space has its own native illuminant, which can vary from space
to space. To see some of these for yourself, check out
Bruce Lindbloom's `XYZ to RGB matrices <http://www.brucelindbloom.com/Eqn_RGB_XYZ_Matrix.html>`_.


To cite the most commonly used RGB color space as an example, sRGB has a
native illuminant of D65. When we convert RGB to XYZ, that native illuminant
carries over unless explicitly overridden. If you aren't expecting this behavior,
you'll end up with variations in your converted color's numbers.

To explicitly request a specific illuminant, provide the ``target_illuminant``
keyword when using :py:func:`colormath.color_conversions.convert_color`.

.. code-block:: python

    from colormath.color_objects import XYZColor, sRGBColor
    from colormath.color_conversions import convert_color

    rgb = RGBColor(0.1, 0.2, 0.3)
    xyz = convert_color(rgb, XYZColor, target_illuminant='d50')

RGB conversions and out-of-gamut coordinates
--------------------------------------------

RGB spaces tend to have a smaller gamut than some of the CIE color spaces.
When converting to RGB, this can cause some of the coordinates to end up
being out of the acceptable range (0.0-1.0 or 1-255, depending on whether
your RGB color is upscaled).

Rather than clamp these for you, we leave them as-is. This allows for more
accurate conversions back to the CIE color spaces. If you require the clamped
(0.0-1.0 or 1-255) values, use the following properties on any RGB color:

* ``clamped_rgb_r``
* ``clamped_rgb_g``
* ``clamped_rgb_b``
