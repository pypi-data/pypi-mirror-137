Matplotlib-sixel backend
========================

A matplotlib backend which outputs sixel graphics onto the terminal.
The code is inspired by the ipython-notebook matplotlib backend.

.. image:: ./demo.png
   :width: 100 %

Dependencies
------------

* terminal with Sixel support like `xterm <https://invisible-island.net/xterm/>`_, `iterm <https://iterm2.com/>`_ and `mlterm <https://github.com/arakiken/mlterm>`_.
* `imagemagick <https://imagemagick.org/>`_ for converting the graphics.
* `matplotlib <https://matplotlib.org/>`_.

Installation
-------------

::

    pip install matplotlib-sixel

Configuration
-------------

the backend has to be altered. Either in your python session with::

    import matplotlib
    matplotlib.use('module://sixel')

or in your ``matplotlibrc`` file::

    backend: module://sixel

To get the colors in the demo above, you can copy
`this matplotlibrc <./matplotlibrc>`_ and make it your own.
