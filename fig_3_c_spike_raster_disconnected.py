# figure_2_c_nosynapse_spikeraster.py --- 
# 
# Filename: figure_2_c_nosynapse_spikeraster.py
# Description: 
# Author: Subhasis Ray
# Maintainer: 
# Created: Thu Jun 26 14:44:23 2014 (+0530)
# Version: 
# Last-Updated: Sun Jan 10 16:05:03 2016 (-0500)
#           By: subha
#     Update #: 6
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
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 3, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street, Fifth
# Floor, Boston, MA 02110-1301, USA.
# 
# 

# Code:

"""Plots spike rasters for populations when simulated without synaptic
connections.

"""

from collections import defaultdict
import numpy as np
import pylab as plt
from util import makepath
from traubdata import TraubData
from trbhist import get_spiketime_hist
from util import makepath, smooth_gaussian
from config import cellcolor
from plotutil import plot_spike_raster

plt.rc('font', size=12)
plt.rc('figure', figsize=(3, 4))

unconnected_filename = 'data_20140423_101740_1735.h5'

if __name__ == '__main__':
    figfilename = 'figures/Figure_3C_spike_raster_disconnected.png'
    trange = (5, 6)
    fig, ax = plot_spike_raster(makepath(unconnected_filename), trange)
    plt.savefig(figfilename, transparent=True)
    plt.show()
    

# 
# figure_2_c_nosynapse_spikeraster.py ends here
