.. _color-appearance-models:

.. include:: global.txt

Color Appearance Models
=======================
Color appearance models allow the prediction of perceptual correlates (e.g., lightness, chroma or hue) of a given
surface color under certain viewing conditions (e.g., a certain illuminant, surround or background). The complexity of
color appearance models can range from very low, e.g., CIELAB can technically be considered a color appearance model,
to very complex models that take into account a large number color appearance phenomena.

Each of the classes in this module represents a specific model and its computation, yielding the predicted perceptual
correlates as instance attributes.
Discussing the details of each model go beyond this documentation, but we provide references to the relevant
literature for each model and would advice familiarising yourself with it, before using a given models.


Example
-------

.. code-block:: python

    # Color stimulus
    color = XYZColor(19.01, 20, 21.78)

    # The two illuminants that will be compared.
    illuminant_d65 = XYZColor(95.05, 100, 108.88)
    illuminant_a = XYZColor(109.85, 100, 35.58)

    # Background relative luminance
    y_b = 20

    # Adapting luminance
    l_a = 328.31

    # Surround condition assumed to be average (see CIECAM02 documentation for values)
    c = 0.69
    n_c = 1
    f = 1

    model = CIECAM02(color.xyz_x, color.xyz_y, color.xyz_z,
                     illuminant_d65.xyz_x, illuminant_d65.xyz_y, illuminant_d65.xyz_z,
                     y_b, l_a, c, n_c, f)


Nayatani95 et al. Model
------------------------

.. autoclass:: colormath.color_appearance_models.Nayatani95

Hunt Model
-----------

.. autoclass:: colormath.color_appearance_models.Hunt
   :exclude-members: adjust_white_for_scc

RLAB Model
----------

.. autoclass:: colormath.color_appearance_models.RLAB

ATD95 Model
------------

.. autoclass:: colormath.color_appearance_models.ATD95

LLAB Model
-----------

.. autoclass:: colormath.color_appearance_models.LLAB

CIECAM02 Model
---------------

.. autoclass:: colormath.color_appearance_models.CIECAM02

CIECAM02-m1 Model
------------------

.. autoclass:: colormath.color_appearance_models.CIECAM02m1

