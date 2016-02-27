# figure_1_b.py --- 
# 
# Filename: figure_1_b.py
# Description: 
# Author: Subhasis Ray
# Maintainer: 
# Created: Fri Jun  6 12:07:23 2014 (+0530)
# Version: 
# Last-Updated: Sun Jan 10 15:52:37 2016 (-0500)
#           By: subha
#     Update #: 16
# URL: 
# Keywords: 
# Compatibility: 
# 
# 

# Commentary: 
# 
# 
# 
# 

# Change log:
# 
# 
# 
# 

# Code:

"""Plot the spontaneous activity in the standard simulation.

This should be with 30 deep basket cells as that makes the number of
inhibitory cells 20% of the total. 240 spiny stellate : 30 deep basket
+30 deep LTS

"""
import os
import sys
import numpy as np
from matplotlib import pyplot as plt
from util import makepath
from config import cellcolor, mdict
from plotutil import plot_spike_raster
from traubdata import TraubData, cellcount_tuple

# datafile_figure_1b = 'data_20120922_195344_13808.h5' # This is a simulation with 30 deep basket, fixed snaptic conductance

datafile_figure_2b = 'data_20140724_125424_236053_compute-0-2.local.h5' # normally distributed synaptic conductance

from matplotlib import rc
rc('font', size=12)
rc('figure', figsize=(3, 4))


if __name__ == '__main__':
    figfilename='figures/Figure_2B_spike_raster.png'
    fig, ax = plot_spike_raster(makepath(datafile_figure_2b), (5, 8))
    fig.tight_layout()
    fig.savefig(figfilename, transparent=True)
    print 'Saved figure in %s' % (figfilename)
    plt.show()

# 
# figure_1_b.py ends here
