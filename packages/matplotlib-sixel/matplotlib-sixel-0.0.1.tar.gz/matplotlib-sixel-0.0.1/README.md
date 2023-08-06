Matplotlib-sixel backend
========================

A matplotlib backend which outputs sixel graphics onto the terminal.
The code is inspired by the ipython-notebook matplotlib backend.

![](./demo.gif)

Dependencies
------------

* terminal with Sixel support configured.
* imagemagick (for converting the graphics)
* matplotlib

Installation
-------------

    pip install matplotlib-sixel

Usage
-----

the backend has to be altered. Either in your python session with:

    import matplotlib
    matplotlib.use('module://matplotlib-sixel')

or in your `matplotlibrc` file:

    backend: module://matplotlib-sixel

With everything in place, plotting should now be sent to terminal output.
