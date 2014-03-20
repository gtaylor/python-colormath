.. _delta-e:

.. include:: global.txt

Delta E Equations
=================

Delta E equations are used to put a number on the visual difference between two
:py:class:`LabColor <colormath.color_objects.LabColor>` instances. While
different lighting conditions, substrates, and physical condition can all
introduce unexpected variables, these equations are a good rough starting point
for comparing colors.

Each of the following Delta E functions has different characteristics. Some may
be more suitable for certain applications than others. While it's outside the
scope of this module's documentation to go into much detail, we link to
relevant material when possible.

Example
-------

.. code-block:: python

    from colormath.color_objects import LabColor
    from colormath.color_diff import delta_e_cie1976

    # Reference color.
    color1 = LabColor(lab_l=0.9, lab_a=16.3, lab_b=-2.22)
    # Color to be compared to the reference.
    color2 = LabColor(lab_l=0.7, lab_a=14.2, lab_b=-1.80)
    # This is your delta E value as a float.
    delta_e = delta_e_cie1976(color1, color2)

Delta E CIE 1976
----------------

.. autofunction:: colormath.color_diff.delta_e_cie1976


Delta E CIE 1994
----------------

.. autofunction:: colormath.color_diff.delta_e_cie1994

Delta E CIE 2000
----------------

.. autofunction:: colormath.color_diff.delta_e_cie2000

Delta E CMC
-----------

.. autofunction:: colormath.color_diff.delta_e_cmc
