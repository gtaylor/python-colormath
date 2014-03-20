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

.. code-block:: python

    from colormath.color_objects import LabColor, RGBColor
    from colormath.color_conversions import convert_color

    lab = LabColor(0.903, 16.296, -2.22)
    xyz = convert_color(lab, XYZColor)
