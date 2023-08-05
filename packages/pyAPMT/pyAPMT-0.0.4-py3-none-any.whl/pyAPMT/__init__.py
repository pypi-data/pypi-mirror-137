# -*- coding: utf-8 -*-

# Author: Sebastian Avalos <sebastian.avalos@apmodtech.com>
#         Advanced Predictive Modeling Technology
#         www.apmodtech.com/pyAPMT/
#         Jan-2022
#
# License: MIT License


# All submodules and packages
from . import Geostatistics
#from . import bregman


# pyAPMT functions
from .Geostatistics.Drill_Holes import DrillHoles


# utils functions
#from .utils import dist, unif, tic, toc, toq

__version__ = "0.0.1"

__requires__ = ['numpy','pandas', 'matplotlib']


#__all__ = ['Geostatistics', 'Contact_Analysis']