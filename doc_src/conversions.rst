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
