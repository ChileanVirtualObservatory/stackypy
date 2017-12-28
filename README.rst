.. image:: https://img.shields.io/readthedocs/stackypy.svg
    :target: http://stackypy.readthedocs.io/en/latest/stack.html

stackypy
----------

Python library to stack images of galaxies and other astronomical objects.

On a series of images the central object is detected after applying a threshold filter, the object is then modeled as an ellipse.

Each Image is scaled, rotated and translated, so that the position and shape of their ellipses match the position and shape of the one on the first image. After that, all the images are added together which results on an image that displays a "mean object".


Go to the `documentation`_.

.. _documentation: http://stackypy.readthedocs.io/en/latest/stack.html
