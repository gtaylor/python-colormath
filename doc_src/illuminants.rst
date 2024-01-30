.. _illuminants:

.. include:: global.txt

Observers and Illuminants
=========================

Illuminants and observer angles are used in all color spaces that use
reflective (instead of transmissive) light. Here are a few brief overviews
of what these are and what they do:

* `Understanding Standard Illuminants in Color Measurement`_ - Konica Minolta
* `What is Meant by the Term "Observer Angle"?`_ - XRite

To adjust the illuminants and/or observer angles on a color::

    lab = LabColor(0.1, 0.2, 0.3, observer='10', illuminant='d65')

Two-degree observer angle
-------------------------

These illuminants can be used with ``observer='2'``, for the color spaces
that require illuminant/observer:

* ``'a'``
* ``'b'``
* ``'c'``
* ``'d50'``
* ``'d55'``
* ``'d65'``
* ``'d75'``
* ``'e'``
* ``'f2'``
* ``'f7'``
* ``'f11'``

Ten-degree observer angle
-------------------------

These illuminants can be used with ``observer='10'``, for the color spaces
that require illuminant/observer:

* ``'d50'``
* ``'d55'``
* ``'d65'``
* ``'d75'``

.. _Understanding Standard Illuminants in Color Measurement: https://sensing.konicaminolta.us/us/blog/understanding-standard-illuminants-in-color-measurement/
.. _What is Meant by the Term "Observer Angle"?: https://www.xrite.com/service-support/what_is_meant_by_the_term_observer_angle
