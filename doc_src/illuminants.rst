.. _illuminants:

.. include:: global.txt

Observers and Illuminants
=========================

Illuminants and observer angles are used in all color spaces that use
reflective (instead of transmissive) light. Here are a few brief overviews
of what these are and what they do:

* `Understanding Standard Illuminants in Color Measurement <understanding illuminants>`_ - Konica Minolta
* `What is Meant by the Term "Observer Angle"? <observer angle>`_ - XRite

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

.. _understanding illuminants: http://sensing.konicaminolta.us/2013/11/Understanding-Standard-Illuminants-in-Color-Measurement/
.. _observer angle: http://www.xrite.com/product_overview.aspx?ID=773&Action=support&SupportID=3544
