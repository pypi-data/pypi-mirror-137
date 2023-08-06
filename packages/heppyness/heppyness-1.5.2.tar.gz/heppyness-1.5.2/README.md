# Heppy

Heppy provides pythonic data structures and a few high-level tools for high energy physics. In particular, it provides very useful histogram classes.

The documentation can be found [here](https://heppy.readthedocs.io).

This package depends on (py)ROOT and this dependency is not automatically handled by pip. Please ensure that you have ROOT with pyROOT installed. Since ROOT is only needed for reading histograms in from ROOT files, it could be made an optional dependency, or eliminated altogether by using [uproot](https://github.com/scikit-hep/uproot). If you'd like me to do either of these things, please get in touch.
